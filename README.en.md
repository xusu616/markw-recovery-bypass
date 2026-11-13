# Redmi 4 Prime / markw: EDL Bootloader Bypass & TWRP Guide

[中文](README.md)

Tested on **Xiaomi Redmi 4 Prime** (`markw`, Snapdragon 625 / MSM8953), originally running MIUI 8 (`V8.2.1.0` series `aboot`).

> **Note**: This is a boot-verification bypass on a locked bootloader, **not** an official bootloader unlock. Both `aboot` and `abootbak` remain unmodified Xiaomi-signed binaries; standard `fastboot` flashing restrictions still apply.

## Verified Components

| Component | File Used | Status |
| --- | --- | --- |
| `aboot` / `abootbak` | Official MIUI `V8.0.5.0.MBECNDG` signed MBN (zero-padded to 1 MiB) | Flashed via EDL and verified |
| Initial recovery | `cofface_twrp_recovery_markw_1121-appended.img` (+4096-byte footer) | Booted into TWRP (ADB root active) |
| Treble recovery | `twrp_3.7.0_12-1-markw_by_SonicBSV_18_11_2023-appended.img` (+4096-byte footer) | Flashed and booted into TWRP 3.7.0 |
| Boot trigger | `misc-boot-recovery-512B.bin` (`boot-recovery\0` in `misc`) | Verified direct boot to TWRP; cleared |
| Footer tool | `scripts/append-boot-footer.py` | Verified on recovery images and ROM `boot.img` |
| Custom ROM | `crDroidAndroid-14.0-20240803-markw-v10.6.zip` (Android 14, Linux `4.9.337`) | Flashed and booted (`ro.crypto.state=unsupported`, built-in `CONFIG_KSU=y`) |
| Root manager | `KernelSU_v0.9.5_11872-release.apk` (`me.weishu.kernelsu`) | Detected built-in KernelSU after reinstall |

## Repository Layout

```text
README.md / README.en.md  Chinese and English guides
LICENSE                   MIT License
scripts/                  EDL backup/flash and boot-footer scripts
payloads/                 V8.0.5.0 aboot, misc trigger image, rawprogram XMLs
roms/                     markw TWRP & ROM images (binaries gitignored)
tools/                    emmcdl 2.16 & MSM8953 Firehose (binaries gitignored)
docs/                     Diagnosis & ROM selection notes
local-only/               Device-specific backups & logs (gitignored)
SHA256SUMS.txt            Verified SHA-256 checksums
```

## Quick Workflow

1. **Read-only GPT & partition backup**:
   ```powershell
   python .\scripts\wait_and_dump_markw_gpt.py
   ```
2. **Flash `V8.0.5.0` `aboot`/`abootbak`, appended TWRP, and `misc` in one Firehose session**:
   ```powershell
   python .\scripts\flash_markw_miui8_aboot_and_twrp.py
   ```
   Unplug USB, reconnect the battery flex, and press Power once to boot directly into TWRP.
3. **Upgrade recovery & flash custom ROM**: For Android 11–14 Treble ROMs, flash the footer-appended `twrp_3.7.0_12-1-markw_by_SonicBSV_18_11_2023-appended.img` to `recovery`, reboot to TWRP 3.7.0, format `/data` if migrating from stock MIUI FDE, wipe `cache`/`dalvik`/`system`, and install the ROM ZIP.
4. **Before rebooting into any custom ROM**, extract `boot.img` from the ROM ZIP, append the 4096-byte footer with `scripts/append-boot-footer.py`, and flash it to `/dev/block/bootdevice/by-name/boot` before rebooting (with `misc` zeroed).
5. **Rollback**: Run `python .\scripts\restore_markw_original_aboot.py` in 9008 EDL mode using your device's original backups in `local-only/markw-diagnosis-20261112/`.

## Download Links

- **SonicBSV `markw` directory (AndroidFileHost)**: [flid=339504](https://androidfilehost.com/?w=files&flid=339504)
- **TWRP `3.7.0_12-1` for Treble ROMs**:
  - `twrp_3.7.0_12-1-markw_by_SonicBSV_18_11_2023.img`: [fid=16385555061192795609](https://androidfilehost.com/?fid=16385555061192795609)
  - `twrp_3.7.0_12-1-markw_by_SonicBSV.img`: [fid=4279422670115717343](https://androidfilehost.com/?fid=4279422670115717343)
- **ROM builds**:
  - `crDroidAndroid-14.0-20240803-markw-v10.6.zip` (Android 14, verified): [fid=6586087556536863991](https://androidfilehost.com/?fid=6586087556536863991)
  - `crDroidAndroid-13.0-20231128-markw-v9.11.zip` (Android 13): [fid=16385555061192797663](https://androidfilehost.com/?fid=16385555061192797663)
- **KernelSU manager** (for the built-in non-GKI `CONFIG_KSU=y` kernel in crDroid v10.6): [KernelSU v0.9.5](https://github.com/tiann/KernelSU/releases/tag/v0.9.5) (`KernelSU_v0.9.5_11872-release.apk`)
- Additional ROM options are listed in [ROM-SELECTION.md](docs/ROM-SELECTION.md).

## License

[MIT](LICENSE)
