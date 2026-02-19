"""Clone the font, drop CFF/sbix (and optionally glyf/loca), then add CBDT/CBLC."""

from __future__ import annotations

from fontTools.ttLib import TTFont
from fontTools.ttLib.tables import DefaultTable

# CFF, sbix, etc. We keep glyf/loca for Windows and morx for ZWJ/sequences.
TABLES_TO_DROP = [
    "cvt ",
    "fpgm",
    "prep",
    "CFF ",
    "CFF2",
    "VORG",
    "sbix",
]

# Tables to drop for Linux.
LINUX_EXTRA_DROP = ["DSIG", "GDEF", "GPOS", "bgcl", "feat", "meta", "morx", "trak"]


def drop_tables(
    font: TTFont,
    extra: list[str] | None = None,
    *,
    keep_outlines: bool = True,
    linux_strip: bool = False,
) -> None:
    tags = list(TABLES_TO_DROP)
    if not keep_outlines:
        tags = tags + ["glyf", "loca"]
    if linux_strip:
        tags = tags + LINUX_EXTRA_DROP
    if extra:
        tags = tags + extra
    for tag in tags:
        if tag in font:
            del font[tag]


def add_raw_table(font: TTFont, tag: str, data: bytes) -> None:
    """Stick a raw table in the font (e.g. CBDT, CBLC)."""
    table = DefaultTable.DefaultTable(tag)
    table.data = data
    font[tag] = table


def build_skeleton(
    font: TTFont,
    cbdt_bytes: bytes,
    cblc_bytes: bytes,
    *,
    drop_vertical: bool = False,
    keep_outlines: bool = True,
    add_bitmap_tables: bool = True,
    linux_strip: bool = False,
) -> None:
    """Drop tables, optionally strip vertical, then add CBDT/CBLC if requested."""
    drop_tables(font, keep_outlines=keep_outlines, linux_strip=linux_strip)
    if drop_vertical:
        for tag in ("vhea", "vmtx"):
            if tag in font:
                del font[tag]

    if add_bitmap_tables:
        add_raw_table(font, "CBDT", cbdt_bytes)
        add_raw_table(font, "CBLC", cblc_bytes)
