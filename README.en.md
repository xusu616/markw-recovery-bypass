# Redmi 4 Prime / markw: EDL Bootloader Bypass & TWRP Guide

[中文](README.md)

Tested on **Xiaomi Redmi 4 Prime** (`markw`, Snapdragon 625 / MSM8953), originally running MIUI 8 (`V8.2.1.0` series `aboot`).

> **Note**: This is a boot-verification bypass on a locked bootloader, **not** an official bootloader unlock. Both `aboot` and `abootbak` remain unmodified Xiaomi-signed binaries; standard `fastboot` flashing restrictions still apply.

## Verified Components

| Component | File Used | Status |
| --- | --- | --- |
| `aboot` / `abootbak` | Official MIUI `V8.0.5.0.MBECNDG` signed MBN (zero-padded to 1 MiB) | Flashed via EDL and verified |
| Initial recovery | `cofface_twrp_recovery_markw_1121-appended.img` (+4096-byte footer) | Booted into TWRP (ADB root active) |
| Boot trigger | `misc-boot-recovery-512B.bin` (`boot-recovery\0` in `misc`) | Verified direct boot to TWRP; auto-cleared |
| Footer tool | `scripts/append-boot-footer.py` | Verified on recovery; required for ROM `boot.img` |
| Custom ROM | Pending selection (see [ROM-SELECTION.md](docs/ROM-SELECTION.md)) | Pending |

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
3. **Before booting any custom ROM**, extract `boot.img` from the ROM ZIP, append the 4096-byte footer with `scripts/append-boot-footer.py`, and flash it to `/dev/block/bootdevice/by-name/boot` before rebooting.
4. **Rollback**: Run `python .\scripts\restore_markw_original_aboot.py` in 9008 EDL mode using your device's original backups in `local-only/markw-diagnosis-20261112/`.

## License

[MIT](LICENSE)
