#!/usr/bin/env python3
"""Apply the pinned HW6728 overlay and BLE Remote autostart patch to Bruce."""

from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
BRUCE = ROOT / "third_party" / "bruce-firmware"
OVERLAY = ROOT / "bruce" / "hw6728"

if not (BRUCE / "platformio.ini").is_file():
    sys.exit("Bruce submodule missing. Run: git submodule update --init --recursive")

board_dst = BRUCE / "boards" / "hw6728-n16r8"
board_dst.mkdir(parents=True, exist_ok=True)
shutil.copy2(OVERLAY / "board" / "hw6728-n16r8.ini", board_dst / "hw6728-n16r8.ini")
shutil.copy2(OVERLAY / "board" / "interface.cpp", board_dst / "interface.cpp")
shutil.copy2(OVERLAY / "partitions_hw6728_n16r8.csv", BRUCE / "partitions_hw6728_n16r8.csv")

main_cpp = BRUCE / "src" / "main.cpp"
source = main_cpp.read_text(encoding="utf-8")
include = '#include "core/settings.h"'
if include not in source:
    anchor = '#include "core/main_menu.h"'
    if anchor not in source:
        sys.exit("Bruce main.cpp changed: cannot find main-menu include anchor")
    source = source.replace(anchor, anchor + "\n" + include, 1)

needle = "    startSerialCommandsHandlerTask(true);"
call = """    startSerialCommandsHandlerTask(true);
#if !defined(LITE_VERSION)
    // HW6728 headless target: expose the Bruce Remote BLE serial API on boot.
    enableBLEAPI();
#endif"""
if "HW6728 headless target: expose the Bruce Remote BLE serial API" not in source:
    if source.count(needle) != 1:
        sys.exit("Bruce main.cpp changed: expected exactly one serial-task startup anchor")
    source = source.replace(needle, call, 1)

main_cpp.write_text(source, encoding="utf-8")
print("HW6728 overlay applied; BLE serial API will start automatically.")
