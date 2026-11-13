"""Reproduce the offline markw images; this script never accesses a device."""
import argparse
import hashlib
import struct
from pathlib import Path

EXPECTED_ABOOT_SHA256 = "ba0294d98ddb7d16b3df16b7c5bae0807550e06cbe28babe0cb6fad487e281a3"
EXPECTED_TWRP_SHA256 = "6599cbbda6b7d2510e8caa8ac2817e49cc6fb7403c877e3d08ddd28ce7af701e"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kind", choices=["aboot", "recovery", "misc"])
    parser.add_argument("source", nargs="?", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    if args.output.exists():
        parser.error("Output already exists; choose a new path.")

    if args.kind == "misc":
        result = b"boot-recovery\x00".ljust(512, b"\x00")
    else:
        if args.source is None:
            parser.error("source is required for aboot and recovery.")
        if args.source.resolve() == args.output.resolve():
            parser.error("Source and output must be different files.")
        data = args.source.read_bytes()
        if args.kind == "aboot":
            if hashlib.sha256(data).hexdigest() != EXPECTED_ABOOT_SHA256:
                parser.error("Source is not the verified MIUI V8.0.5.0 markw MBN.")
            result = data + bytes(1_048_576 - len(data))
        else:
            if hashlib.sha256(data).hexdigest() != EXPECTED_TWRP_SHA256:
                parser.error("Source is not the verified Cofface TWRP 1121 image.")
            kernel, ramdisk, second, page, dt = [
                struct.unpack_from("<I", data, n)[0] for n in (8, 16, 24, 36, 40)
            ]
            align = lambda n: (n + page - 1) // page * page
            end = page + sum(align(n) for n in (kernel, ramdisk, second, dt))
            if data[:8] != b"ANDROID!" or end != len(data):
                parser.error("Unexpected Android boot image layout.")
            result = data + bytes.fromhex("3083198964") + bytes(4091)

    args.output.write_bytes(result)
    print(f"{hashlib.sha256(result).hexdigest()} *{args.output} ({len(result)} bytes)")


if __name__ == "__main__":
    main()
