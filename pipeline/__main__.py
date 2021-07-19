import socket
import typing as t
from dataclasses import asdict
from pathlib import Path

from returns.io import IOSuccess
from returns.iterables import Fold
from returns.pipeline import flow
from returns.pointfree import bind
from returns.result import ResultE, Success, safe

from pipeline.netbox_service.service import get_netbox_devices
from pipeline.templates import TemplateVars, env
from pipeline.vni_service.db import create_connection, create_data
from pipeline.vni_service.service import get_device_ipam_data, get_vni_data

template = env.get_template("switch_template")

# Big, ugly side-effect here, it's a demo. ¯\_(ツ)_/¯
# TODO, use context
CON = create_connection()
create_data(CON)


@safe
def render_device_template(
    device, device_ipam, site_vni_data
) -> t.Tuple[str, t.Dict[str, str]]:
    hostname = device["name"]
    site_name = device["site"]["name"]
    lo5_meta = device_ipam[(hostname, "loopback 5")]
    mgmt_meta = device_ipam[(hostname, "management 1")]
    lo5_cidr = f"{socket.inet_ntop(lo5_meta.addr_family, lo5_meta.ip_address)}/{lo5_meta.netmask}"
    site_svi_desc = f"Routed SVI for site {site_name}"
    site_vni = site_vni_data[site_name].vni
    site_svi_cidr = (
        f"{socket.inet_ntop(socket.AF_INET, site_vni_data[site_name].ip_address)}/"
        + f"{site_vni_data[site_name].netmask}"
    )
    management_ip_cidr = (
        f"{socket.inet_ntop(mgmt_meta.addr_family, mgmt_meta.ip_address)}/"
        + f"{mgmt_meta.netmask}"
    )
    template_vars = TemplateVars(
        hostname=hostname,
        lo5_cidr=lo5_cidr,
        site_svi_desc=site_svi_desc,
        site_vni=site_vni,
        site_svi_cidr=site_svi_cidr,
        management_ip_cidr=management_ip_cidr,
    )
    return hostname, template.render(asdict(template_vars))


def render_all(ext_data):
    devices, vni_data = ext_data
    return Fold.collect(
        map(
            lambda device: get_device_ipam_data(CON, device["name"]).bind(
                lambda ipam: render_device_template(device, ipam, vni_data)
            ),
            devices,
        ),
        Success(()),
    )


@safe
def write_configs_to_file(devices: t.Dict[str, ResultE[str]], basepath: str) -> None:
    path = Path(basepath)
    for hostname, template in devices:
        with open(path.joinpath(hostname), "w") as fp:
            fp.write(template)


def run() -> t.Dict[str, t.Any]:
    Fold.collect([get_netbox_devices(), get_vni_data(CON)], IOSuccess(())).bind(
        render_all
    ).bind(lambda devices: write_configs_to_file(devices, "output")).unwrap()


if __name__ == "__main__":
    run()
