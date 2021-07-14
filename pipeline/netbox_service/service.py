import typing as t

import httpx

NETBOX_URL = "https://netboxdemo.com"
NETBOX_API_TOKEN = " 72830d67beff4ae178b94d8f781842408df8069d"


def get_netbox_devices(mock=True) -> t.List[t.Any]:
    if mock:
        from pipeline.netbox_service.mock_data import nb_data

        return nb_data
    devices = httpx.get(
        f"{NETBOX_URL}/api/dcim/devices/",
        headers={
            "Authorization": f"Token {NETBOX_API_TOKEN}",
            "Accept": "application/json",
        },
    ).json()["results"]
    return devices
