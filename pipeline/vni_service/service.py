import socket
import typing as t
from dataclasses import dataclass
from returns.io import IOResultE, impure_safe


@dataclass
class L3vniRow:
    vni: int
    addr_family: int
    ip_address: int
    netmask: int
    site: str


@dataclass
class DeviceIPAMRow:
    addr_family: int
    ip_address: int
    netmask: int
    interface: str
    device: str


def get_af(af: int):
    if af == 4:
        family = socket.AF_INET
    elif af == 6:
        family = socket.AF_INET6
    return family


def l3vni_row_factory(cursor, row) -> L3vniRow:
    """Row factory to load l3vni data into an L3vniRow class."""
    return L3vniRow(row[0], get_af(row[1]), row[2], row[3], row[4].decode("utf-8"))


@impure_safe
def get_vni_data(con) -> t.Dict[str, t.Any]:
    """Retreive vni data rows"""
    con.row_factory = l3vni_row_factory
    with con:
        data = con.execute("SELECT * FROM l3vni")
    site_data = {}
    for row in data:
        site_data[row.site] = row
    con.row_factory = None
    return site_data


def device_ipam_row_factory(cursor, row) -> DeviceIPAMRow:
    """Row factory to load l3vni data into an DeviceIPAMRow class."""
    return DeviceIPAMRow(
        get_af(row[0]), row[1], row[2], row[3].decode("utf-8"), row[4].decode("utf-8")
    )


@impure_safe
def get_device_ipam_data(con) -> t.Dict[t.Tuple[str, str], t.Any]:
    """Retreive device IPAM rows"""
    con.row_factory = device_ipam_row_factory
    with con:
        data = con.execute("SELECT * FROM device_ipam")
    device_data = {}
    for row in data:
        device_data[(row.device, row.interface)] = row
    con.row_factory = None
    return device_data
