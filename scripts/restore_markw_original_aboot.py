# -*- coding: utf-8 -*-
"""
Redmi 4 Prime (markw / MSM8953) Restore Original Signed Aboot via 9008 EDL
"""
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
EMMCDL = TOOLS / "emmcdl-2.16.exe"
FIREHOSE = TOOLS / "prog_emmc_firehose_8953_ddr.mbn"
RESTORE_DIR = ROOT / "local-only" / "markw-diagnosis-20261112"
XML_FILE = RESTORE_DIR / "rawprogram_markw_restore.xml"


def find_9008_port():
    try:
        import serial.tools.list_ports

        for p in serial.tools.list_ports.comports():
            desc = (p.description or "").lower()
            hwid = (p.hwid or "").lower()
            if "9008" in desc or ("05c6" in hwid and "9008" in hwid):
                return p.device
    except Exception:
        pass
    try:
        out = subprocess.check_output(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "Get-CimInstance Win32_PnPEntity | Where-Object { $_.Name -like '*9008*' } | Select-Object -ExpandProperty Name",
            ],
            text=True,
            stderr=subprocess.DEVNULL,
            timeout=5,
        )
        m = re.search(r"\((COM\d+)\)", out, re.IGNORECASE)
        if m:
            return m.group(1).upper()
    except Exception:
        pass
    return None


def main():
    print("=" * 70)
    print("红米 4 高配版 (markw / MSM8953) 9008 救砖: 恢复官方原版已签名 aboot/abootbak")
    print("=" * 70)

    if not XML_FILE.exists():
        print(f"[错误] 描述 XML 文件不存在: {XML_FILE}")
        sys.exit(1)

    print("\n[待恢复任务]:")
    print("  1. aboot 分区    (LBA 786432) -> aboot.bin (官方原厂签名引导)")
    print("  2. abootbak 分区 (LBA 788480) -> abootbak.bin (官方原厂签名备份)")

    print("\n[提示] 请拔下数据线、断开电池排线 5 秒，然后短接测试点并插入 USB 数据线...")
    print("等待 9008 COM 端口连接中", end="", flush=True)

    port = None
    while not port:
        port = find_9008_port()
        if port:
            break
        print(".", end="", flush=True)
        time.sleep(0.5)

    print(f"\n\n[已连接] 检测到 9008 端口: {port}！开始恢复原厂引导...")

    cmd = [
        str(EMMCDL),
        "-p", port,
        "-f", str(FIREHOSE),
        "-MaxPayloadSizeToTargetInBytes", "16384",
        "-x", str(XML_FILE.name),
    ]

    print(f"\n>> [执行命令] {' '.join(cmd)}\n")
    ret = subprocess.run(cmd, cwd=str(RESTORE_DIR))

    if ret.returncode != 0:
        print(f"\n[错误] 烧录异常，emmcdl 退出码: {ret.returncode}")
        sys.exit(ret.returncode)

    print("\n" + "=" * 70)
    print("★ 恢复成功！原厂 aboot 与 abootbak 已写回！")
    print("=" * 70)
    print("现在可以正常开机或按住【音量下 + 电源键】进入 Fastboot 了！")


if __name__ == "__main__":
    main()
