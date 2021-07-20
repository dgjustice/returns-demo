"""DB utilities for our VNI service."""

import sqlite3
import typing as t

from pipeline.app_config import SQLITE_DB_NAME


def create_connection() -> t.Any:
    con = sqlite3.connect(SQLITE_DB_NAME)
    con.text_factory = bytes
    return con


def create_data(con) -> None:
    with con:
        con.execute(
            "CREATE TABLE l3vni "
            + "(vni INTEGER, addr_family INTEGER, ip_address BLOB, netmask INTEGER, site TEXT)"
        )
        con.executemany(
            """INSERT INTO l3vni VALUES (?, ?, ?, ?, ?)""",
            (
                (54321, 4, b"\n\x00d\x01", 24, "DS9"),
                (98765, 4, b"\nd\x00\x01", 24, "NCC-1701-D"),
            ),
        )
        con.execute(
            "CREATE TABLE device_ipam "
            + "(addr_family INTEGER, ip_address BLOB, netmask INTEGER, interface TEXT, device TEXT)"
        )
        con.executemany(
            """INSERT INTO device_ipam VALUES (?, ?, ?, ?, ?)""",
            (
                (4, b"\xc0\xa8\x00\xc2", 24, "loopback 5", "1701_CORE_SWITCH"),
                (4, b"\xac\x114\xcc", 24, "management 1", "1701_CORE_SWITCH"),
                (4, b"\xc0\xa8\x00\x0e", 24, "loopback 5", "1701_FW"),
                (4, b"\xac\x114.", 24, "management 1", "1701_FW"),
                (4, b"\xc0\xa8\x00\xf2", 24, "loopback 5", "1701_MDF_ACCESS-sw1"),
                (4, b"\xac\x114\x1b", 24, "management 1", "1701_MDF_ACCESS-sw1"),
                (4, b"\xc0\xa8\x00\x87", 24, "loopback 5", "1701_MDF_ACCESS-sw2"),
                (4, b"\xac\x114@", 24, "management 1", "1701_MDF_ACCESS-sw2"),
                (4, b"\xc0\xa8\x00\xdd", 24, "loopback 5", "1701_MDF_R1_PDU_A"),
                (4, b"\xac\x114\xf1", 24, "management 1", "1701_MDF_R1_PDU_A"),
                (4, b"\xc0\xa8\x00\x9d", 24, "loopback 5", "1701_MDF_R1_PDU_B"),
                (4, b"\xac\x114\xae", 24, "management 1", "1701_MDF_R1_PDU_B"),
                (4, b"\xc0\xa8\x00\xe9", 24, "loopback 5", "1701_MDF_R1_U40"),
                (4, b"\xac\x114\x11", 24, "management 1", "1701_MDF_R1_U40"),
                (4, b"\xc0\xa8\x000", 24, "loopback 5", "1701_MDF_R1_U41"),
                (4, b"\xac\x114\x8d", 24, "management 1", "1701_MDF_R1_U41"),
                (4, b"\xc0\xa8\x00\xfe", 24, "loopback 5", "1701_MDF_R1_U42"),
                (4, b"\xac\x114\xed", 24, "management 1", "1701_MDF_R1_U42"),
                (4, b"\xc0\xa8\x00\xb0", 24, "loopback 5", "1701_RR_ACCESS"),
                (4, b"\xac\x114\x9c", 24, "management 1", "1701_RR_ACCESS"),
                (4, b"\xc0\xa8\x00\xeb", 24, "loopback 5", "1701_RR_IDF_PDU"),
                (4, b"\xac\x114\xad", 24, "management 1", "1701_RR_IDF_PDU"),
                (4, b"\xc0\xa8\x006", 24, "loopback 5", "1701_RR_IDF_U7"),
                (4, b"\xac\x114\x85", 24, "management 1", "1701_RR_IDF_U7"),
                (4, b"\xc0\xa8\x00\xf6", 24, "loopback 5", "1701_RR_IDF_U8"),
                (4, b"\xac\x114\x19", 24, "management 1", "1701_RR_IDF_U8"),
                (4, b"\xc0\xa8\x00\xcf", 24, "loopback 5", "DS9_CORE_ACCESS"),
                (4, b"\xac\x114\xf3", 24, "management 1", "DS9_CORE_ACCESS"),
                (4, b"\xc0\xa8\x00a", 24, "loopback 5", "DS9_CORE_FIBER_U42"),
                (4, b"\xac\x114j", 24, "management 1", "DS9_CORE_FIBER_U42"),
                (4, b"\xc0\xa8\x004", 24, "loopback 5", "DS9_CORE_PDU_A"),
                (4, b"\xac\x114K", 24, "management 1", "DS9_CORE_PDU_A"),
                (4, b"\xc0\xa8\x00\xac", 24, "loopback 5", "DS9_CORE_PDU_B"),
                (4, b"\xac\x114\xf7", 24, "management 1", "DS9_CORE_PDU_B"),
                (4, b"\xc0\xa8\x00\xbf", 24, "loopback 5", "DS9_CORE_SWITCH"),
                (4, b"\xac\x114\x85", 24, "management 1", "DS9_CORE_SWITCH"),
                (4, b"\xc0\xa8\x00]", 24, "loopback 5", "DS9_CORE_U41"),
                (4, b"\xac\x114x", 24, "management 1", "DS9_CORE_U41"),
                (4, b"\xc0\xa8\x00\xe0", 24, "loopback 5", "DS9_FW"),
                (4, b"\xac\x114F", 24, "management 1", "DS9_FW"),
                (4, b"\xc0\xa8\x00\xaa", 24, "loopback 5", "DS9_QUARKS_ACCESS"),
                (4, b"\xac\x114\xd8", 24, "management 1", "DS9_QUARKS_ACCESS"),
                (4, b"\xc0\xa8\x00\x9a", 24, "loopback 5", "DS9_QUARKS_FIBER_U8"),
                (4, b"\xac\x114\x98", 24, "management 1", "DS9_QUARKS_FIBER_U8"),
                (4, b"\xc0\xa8\x00\xda", 24, "loopback 5", "DS9_QUARKS_PDU"),
                (4, b"\xac\x114^", 24, "management 1", "DS9_QUARKS_PDU"),
                (4, b"\xc0\xa8\x00}", 24, "loopback 5", "DS9_QUARKS_U7"),
                (4, b"\xac\x114_", 24, "management 1", "DS9_QUARKS_U7"),
                (4, b"\xc0\xa8\x00g", 24, "loopback 5", "DS9_SECOFFICE_ACCESS"),
                (4, b"\xac\x1145", 24, "management 1", "DS9_SECOFFICE_ACCESS"),
                (4, b"\xc0\xa8\x00\xca", 24, "loopback 5", "DS9_SECOFFICE_FIBER_U12"),
                (4, b"\xac\x1144", 24, "management 1", "DS9_SECOFFICE_FIBER_U12"),
                (4, b"\xc0\xa8\x00C", 24, "loopback 5", "DS9_SECOFFICE_PDU"),
                (4, b"\xac\x114\xfb", 24, "management 1", "DS9_SECOFFICE_PDU"),
                (4, b"\xc0\xa8\x00\xe6", 24, "loopback 5", "DS9_SECOFFICE_U11"),
                (4, b"\xac\x114\x10", 24, "management 1", "DS9_SECOFFICE_U11"),
            ),
        )
