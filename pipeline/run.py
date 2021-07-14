import socket
import typing as t
from dataclasses import asdict

from pipeline.netbox_service.service import get_netbox_devices
from pipeline.templates import TemplateVars, env
from pipeline.vni_service.db import create_connection, create_data
from pipeline.vni_service.service import get_device_ipam_data, get_vni_data

template = env.get_template("switch_template")

con = create_connection()
create_data(con)

def render_device_templates() -> t.Dict[str, t.Any]:
    devices = get_netbox_devices()
    device_ipam = get_device_ipam_data(con)
    site_vni_data = get_vni_data(con)
    device_templates = {}
    for device in devices:
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
        device_templates[hostname] = template.render(asdict(template_vars))
    return device_templates


templates = render_device_templates()
print(templates["1701_MDF_ACCESS-sw1"])
