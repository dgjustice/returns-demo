"""Functions to call a 3rd-party Netbox service."""

import typing as t

import httpx
from returns.io import IOResultE, IOSuccess, impure_safe

NETBOX_URL = "https://netboxdemo.com"
NETBOX_API_TOKEN = " 72830d67beff4ae178b94d8f781842408df8069d"


def get_mock_data() -> IOResultE[t.List[t.Dict[str, t.Any]]]:
    """Get data from the local disk and be nice to the internet."""
    from pipeline.netbox_service.mock_data import nb_data

    return IOSuccess(nb_data)


@impure_safe
def get_live_data() -> t.List[t.Dict[str, t.Any]]:
    """Send an API request for inventory to a Netbox instance."""
    devices = httpx.get(
        f"{NETBOX_URL}/api/dcim/devices/",
        headers={
            "Authorization": f"Token {NETBOX_API_TOKEN}",
            "Accept": "application/json",
        },
    ).json()["results"]
    return devices


def get_netbox_devices(mock: bool = True) -> IOResultE[t.List[t.Dict[str, t.Any]]]:
    """Collect an inventory, and don't pick on a third party by default."""
    if mock:
        return get_mock_data()
    return get_live_data()
