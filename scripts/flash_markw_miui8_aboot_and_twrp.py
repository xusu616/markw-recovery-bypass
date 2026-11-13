#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Redmi 4 Prime (markw / MSM8953) 9008 EDL Flash Script (Single-Shot Unified):
Flashes MIUI V8.0.5.0 signed aboot/abootbak, appended Cofface TWRP, and misc boot-recovery flag
in a SINGLE emmcdl invocation.
"""

import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EDL_EXE = ROOT / "tools" / "emmcdl-2.16.exe"
LOADER_MSM8953 = ROOT / "tools" / "prog_emmc_firehose_8953_ddr.mbn"

PAYLOADS_DIR = ROOT / "payloads"
ABOOT_IMG = PAYLOADS_DIR / "aboot-miui8-v8050-signed-1MiB.bin"
ABOOT_ONLY_XML = PAYLOADS_DIR / "rawprogram_markw_miui8_aboot.xml"
RECOVERY_MISC_XML = PAYLOADS_DIR / "rawprogram_markw_recovery_and_misc.xml"
UNIFIED_ALL_XML = PAYLOADS_DIR / "rawprogram_markw_miui8_all.xml"

TWRP_IMG = ROOT / "roms" / "cofface_twrp_recovery_markw_1121-appended.img"
TWRP_LINK_IN_DIR = PAYLOADS_DIR / "cofface_twrp_recovery_markw_1121-appended.img"
MISC_IMG = PAYLOADS_DIR / "misc-boot-recovery-512B.bin"

EXPECTED_ABOOT_SHA256 = "cff1766fc4e6d3db7a9a0b17d24019e09856aeed029fb43a94982bca7d7a60cc"
EXPECTED_ABOOT_LEN = 1_048_576

EXPECTED_TWRP_SHA256 = "dfd363b80ea169621230ab33fefa049d60b99036e757cad35374cc2b7c9b3218"
EXPECTED_TWRP_LEN = 29_509_632

EXPECTED_MISC_SHA256 = "9418492e5b413376d2927de020eecc19a0be271687c4edb6437b7ce7268a2171"
EXPECTED_MISC_LEN = 512


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest().lower()


def find_9008_port() -> str | None:
    try:
        import serial.tools.list_ports

        for p in serial.tools.list_ports.comports():
            desc = (p.description or "").lower()
            hwid = (p.hwid or "").lower()
            if "9008" in desc or ("05c6" in hwid and "9008" in hwid):
                return p.device
    except Exception:
        pass

    cmd = [
        "powershell",
        "-NoProfile",
        "-Command",
        "Get-CimInstance Win32_PnPEntity | "
        "Where-Object { $_.Name -match 'Qualcomm HS-USB QDLoader 9008 \\((COM\\d+)\\)' } | "
        "ForEach-Object { $_.Name }",
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=3)
        for line in res.stdout.splitlines():
            m = re.search(r"\((COM\d+)\)", line)
            if m:
                return m.group(1)
    except Exception:
        pass
    return None


def beep(ok: bool = True) -> None:
    try:
        import winsound

        if ok:
            winsound.Beep(1200, 250)
            winsound.Beep(1600, 350)
        else:
            winsound.Beep(500, 500)
    except Exception:
        pass


def run_edl(port: str, args: list[str], cwd: Path) -> int:
    cmd = [
        str(EDL_EXE),
        "-p",
        port,
        "-f",
        str(LOADER_MSM8953),
        "-MaxPayloadSizeToTargetInBytes",
        "16384",
        *args,
    ]
    print(f"\n>> [执行单次原子烧录] (cwd={cwd})\n   {' '.join(cmd)}\n")
    res = subprocess.run(cmd, cwd=str(cwd))
    return res.returncode


def verify_input_file(path: Path, expected_len: int, expected_sha256: str, label: str) -> None:
    if not path.is_file():
        print(f"[错误] {label} 文件不存在: {path}")
        sys.exit(1)
    actual_len = path.stat().st_size
    if actual_len != expected_len:
        print(f"[错误] {label} 大小异常: {actual_len} 字节 (预期 {expected_len})")
        sys.exit(1)
    actual_hash = sha256_file(path)
    if actual_hash != expected_sha256:
        print(f"[错误] {label} SHA-256 校验失败: {actual_hash} (预期 {expected_sha256})")
        sys.exit(1)
    print(f"  [OK] {label}: {path.name} ({actual_len} 字节, SHA-256: {actual_hash[:16]}...)")


def ensure_twrp_in_payloads_dir() -> None:
    if not TWRP_LINK_IN_DIR.is_file():
        try:
            os.link(str(TWRP_IMG), str(TWRP_LINK_IN_DIR))
        except Exception:
            shutil.copy2(str(TWRP_IMG), str(TWRP_LINK_IN_DIR))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="红米 4 高配版 (markw) 9008 单次原子烧录工具 (MIUI V8.0.5.0 aboot / TWRP)"
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--twrp-only", action="store_true", help="仅刷入 TWRP 与 misc boot-recovery 标志 (aboot 已刷成功时推荐)")
    mode.add_argument("--aboot-only", action="store_true", help="仅单独刷入 MIUI V8.0.5.0 aboot 与 abootbak")
    args = parser.parse_args()

    print("=" * 72)
    print("红米 4 高配版 (markw / MSM8953) 9008 单次原子烧录工具")
    print("=" * 72)

    for required, name in [(EDL_EXE, "emmcdl-2.16.exe"), (LOADER_MSM8953, "Firehose Loader")]:
        if not required.is_file():
            print(f"[错误] 缺少必要工具 {name}: {required}")
            sys.exit(1)

    if args.twrp_only:
        verify_input_file(TWRP_IMG, EXPECTED_TWRP_LEN, EXPECTED_TWRP_SHA256, "TWRP (Appended)")
        verify_input_file(MISC_IMG, EXPECTED_MISC_LEN, EXPECTED_MISC_SHA256, "misc boot-recovery")
        ensure_twrp_in_payloads_dir()
        flash_mode = "twrp_only"
        print("\n[待烧录任务]: 单个 XML 连续写入 recovery + misc(boot-recovery)，开机直进 TWRP")
    elif args.aboot_only:
        verify_input_file(ABOOT_IMG, EXPECTED_ABOOT_LEN, EXPECTED_ABOOT_SHA256, "MIUI V8.0.5.0 aboot")
        flash_mode = "aboot_only"
        print("\n[待烧录任务]: 单次写入 aboot 与 abootbak 分区")
    else:
        verify_input_file(ABOOT_IMG, EXPECTED_ABOOT_LEN, EXPECTED_ABOOT_SHA256, "MIUI V8.0.5.0 aboot")
        verify_input_file(TWRP_IMG, EXPECTED_TWRP_LEN, EXPECTED_TWRP_SHA256, "TWRP (Appended)")
        verify_input_file(MISC_IMG, EXPECTED_MISC_LEN, EXPECTED_MISC_SHA256, "misc boot-recovery")
        ensure_twrp_in_payloads_dir()
        flash_mode = "all_in_one"
        print("\n[待烧录任务]: 单个 XML 会话一次性连续写入 aboot + abootbak + recovery + misc(boot-recovery)")

    print("\n[提示] 请断开电池排线 5 秒彻底放电，短接 EDL 测试点后插入 USB 数据线...")
    port = None
    dots = 0
    while not port:
        port = find_9008_port()
        if not port:
            dots = (dots + 1) % 4
            sys.stdout.write(f"\r等待 9008 COM 端口连接{'.' * dots}   ")
            sys.stdout.flush()
            time.sleep(0.5)

    print(f"\n\n[已连接] 检测到 9008 端口: {port}，保持短接稳定...")

    if flash_mode == "twrp_only":
        print("\n[执行] 正在通过 XML 烧录 TWRP (recovery) 与 boot-recovery 标志 (misc)...")
        rc = run_edl(port, ["-x", RECOVERY_MISC_XML.name], cwd=PAYLOADS_DIR)
    elif flash_mode == "aboot_only":
        print("\n[执行] 正在通过 XML 烧录 aboot/abootbak...")
        rc = run_edl(port, ["-x", ABOOT_ONLY_XML.name], cwd=PAYLOADS_DIR)
    else:
        print("\n[执行] 正在通过统一 XML 连续烧录全部 4 个分区 (aboot + abootbak + recovery + misc)...")
        rc = run_edl(port, ["-x", UNIFIED_ALL_XML.name], cwd=PAYLOADS_DIR)

    if rc != 0:
        beep(ok=False)
        print(f"\n[错误] 烧录未成功完成，emmcdl 返回值: {rc}")
        sys.exit(rc)

    beep(ok=True)
    print("\n" + "=" * 72)
    print("★ 全部烧录成功完成！现在可以松开镊子并拔掉数据线。")
    print("=" * 72)
    print("后续进入 TWRP 步骤：")
    print("  1. 拔掉 USB 数据线，扣紧电池排线；")
    print("  2. 无需任何组合键，直接按一下【电源键】开机（V8.0.5.0 aboot 会读取 misc 直接进 TWRP）；")
    print("  3. 若未写 misc 标志而使用硬按键：必须先拔掉 USB 线彻底关机，再同时按住【音量加 + 音量减 + 电源键】；")
    print("  4. 进入 TWRP 后，确认 misc 已清零（若未清零可运行）：")
    print('     adb shell "dd if=/dev/zero of=/dev/block/bootdevice/by-name/misc bs=512 count=1"')
    print("=" * 72)


if __name__ == "__main__":
    main()
