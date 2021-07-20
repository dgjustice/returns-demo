"""Config store for our service.

This data could come from a variety of sources such as Ansible
or your other favorite YAML-based nightmare."""

GLOBAL_VARS = {"NTP_SERVER_IP_ADDR": "1.1.1.1", "LOGIN_SECRET": "supersecret"}

SQLITE_DB_NAME = ":memory:"
