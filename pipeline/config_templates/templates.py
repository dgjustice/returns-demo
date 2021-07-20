"""Template store for building configuration snippets."""

from dataclasses import dataclass

from jinja2 import DictLoader, Environment, StrictUndefined

from pipeline.app_config import GLOBAL_VARS


@dataclass
class TemplateVars:
    hostname: str
    lo5_cidr: str
    site_svi_desc: str
    site_vni: int
    site_svi_cidr: str
    management_ip_cidr: str
    ntp_server_ip_addr: str = GLOBAL_VARS["NTP_SERVER_IP_ADDR"]
    login_secret: str = GLOBAL_VARS["LOGIN_SECRET"]


switch_template = """hostname {{ hostname }}

ntp server {{ ntp_server_ip_addr }}

username nw-ops role network-admin secret 0 {{ login_secret }}

interface Loopback5
  ip address {{ lo5_cidr }}

interface vxlan 1
  vxlan source-interface loopback 5
  vxlan vlan 100 vni {{ site_vni }}

interface vlan 100
  description {{ site_svi_desc }}
  ip address {{ site_svi_cidr }}

interface Management1
  ip address {{ management_ip_cidr }}
  no shutdown
"""

env = Environment(
    loader=DictLoader({"switch_template": switch_template}), undefined=StrictUndefined
)
