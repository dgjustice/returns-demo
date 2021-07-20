"""Entrypoint to deploy configurations from collected data."""

import socket
import typing as t
from dataclasses import asdict
from pathlib import Path

from returns.context import RequiresContext
from returns.curry import partial
from returns.functions import tap
from returns.io import IOSuccess
from returns.iterables import Fold
from returns.pipeline import flow
from returns.pointfree import bind, map_
from returns.result import ResultE, Success, safe
from returns.context.requires_context import RequiresContext

from pipeline.config_templates.templates import TemplateVars, env
from pipeline.netbox_service.service import get_netbox_devices
from pipeline.vni_service.db import create_connection, create_data
from pipeline.vni_service.service import get_device_ipam_data, get_vni_data


def render_device_template(
    device, device_ipam, site_vni_data
) -> RequiresContext[ResultE[t.Tuple[str, str]], t.Any]:
    """Render a single device configuration template."""
    hostname: str = device["name"]
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
    return RequiresContext(
        safe(lambda template: (hostname, template.render(asdict(template_vars))))
    )


def render_all(ext_data) -> RequiresContext[ResultE[t.Tuple[t.Tuple[str, str]]], t.Any]:
    """Helper function to wrap rendering of all templates."""
    devices, vni_data = ext_data
    return RequiresContext(
        lambda con: Fold.collect(
            map(
                lambda device: get_device_ipam_data(con, device["name"]).map(
                    lambda ipam: render_device_template(  #  type: ignore
                        device, ipam, vni_data
                    )
                ),
                devices,
            ),
            Success(()),
        )
    )


@safe
def write_configs_to_file(
    devices: t.Tuple[t.Tuple[str, str], ...], basepath: str
) -> None:
    """Write device configs to a file."""
    path = Path(basepath)
    for hostname, template in devices:
        with open(path.joinpath(hostname), "w") as fp:
            fp.write(template)


def run() -> None:
    """Do all the things!"""
    con = create_connection()
    create_data(con)
    template = env.get_template("switch_template")
    flow(
        Fold.collect([get_netbox_devices(), get_vni_data(con)], IOSuccess(())),
        map_(render_all),
        bind(lambda res: res(con)),
        bind(partial(map, lambda fn: fn(template))),
        bind(lambda devices: write_configs_to_file(devices, "output")),
    ).unwrap()
    print("Success!")


if __name__ == "__main__":
    run()
