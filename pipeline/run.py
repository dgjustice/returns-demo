import socket
import typing as t
from dataclasses import asdict
from pathlib import Path
from returns.io import IO, IOResult, IOResultE, IOSuccess
from pipeline.netbox_service.service import get_netbox_devices
from pipeline.templates import TemplateVars, env
from pipeline.vni_service.db import create_connection, create_data
from pipeline.vni_service.service import get_device_ipam_data, get_vni_data
from returns.curry import partial
from returns.result import ResultE, safe
from returns.pointfree import bind_result
from returns.iterables import Fold

template = env.get_template("switch_template")

# Big, ugly side-effect here, it's a demo. ¯\_(ツ)_/¯
# TODO, use context
CON = create_connection()
create_data(CON)


@safe
def render_device_template(device, device_ipam, site_vni_data):
    hostname = device["name"]
    site_name = device["site"]["name"]
    lo5_meta = device_ipam[(hostname, "loopback 5")]
    mgmt_meta = device_ipam[(hostname, "management 1")]
    lo5_cidr = f"{socket.inet_ntop(lo5_meta.addr_family, lo5_meta.ip_address)}/{lo5_meta.netmask}"
    site_svi_desc = f"Routed SVI for site {site_name}"
    site_vni = site_vni_data[site_name].vni
    site_svi_cidr = f"{socket.inet_ntop(socket.AF_INET, site_vni_data[site_name].ip_address)}/{site_vni_data[site_name].netmask}"
    management_ip_cidr = f"{socket.inet_ntop(mgmt_meta.addr_family, mgmt_meta.ip_address)}/{mgmt_meta.netmask}"
    template_vars = TemplateVars(
        hostname=hostname,
        lo5_cidr=lo5_cidr,
        site_svi_desc=site_svi_desc,
        site_vni=site_vni,
        site_svi_cidr=site_svi_cidr,
        management_ip_cidr=management_ip_cidr,
    )
    return template.render(asdict(template_vars))


def render_all(ext_data) -> t.Dict[str, ResultE[str]]:
    device_templates = IO({})
    devices = ext_data[0]
    for device in devices:
        device_templates[device["name"]] = get_device_ipam_data(
            CON, device["name"]
        ).bind(lambda ipam: render_device_template(device, ipam, ext_data[1]))
    return device_templates


@safe
def write_configs_to_file(devices: t.Dict[str, ResultE[str]], basepath: str) -> None:
    path = Path(basepath)
    for hostname, template_res in devices.items():
        with open(path.joinpath(hostname), "w") as fp:
            template_res.map(fp.write).unwrap()


def run() -> t.Dict[str, t.Any]:
    Fold.collect([get_netbox_devices(), get_vni_data(CON)], IOSuccess(())).bind(
        render_all
    )
    write_configs_to_file(temps).unwrap()


templates = run()
