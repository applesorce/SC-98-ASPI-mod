#!/usr/bin/env python3
"""Apply the SC-98 ATN byte patch to a verified ASPISC98.SYS Ver.1.06."""

import argparse
import hashlib
from pathlib import Path

ORIGINAL_SIZE = 4355
ORIGINAL_SHA256 = "4f016e4014141ae661aa787490b62eb8038456b2aef3ac36542c52118296c62f"
PATCHED_SHA256 = "cd0d2c90ac659393be05f8493446896b93773f046d0fcd4a1ada8ac5669f85f6"
PATCH_OFFSET = 0x051C


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="original ASPISC98.SYS Ver.1.06")
    parser.add_argument("destination", type=Path, help="patched output file")
    args = parser.parse_args()

    source = args.source.read_bytes()
    if len(source) != ORIGINAL_SIZE or digest(source) != ORIGINAL_SHA256:
        raise SystemExit("error: source size or SHA-256 does not match ASPISC98.SYS Ver.1.06")
    if source[PATCH_OFFSET] != 0x09:
        raise SystemExit("error: expected byte 09h is missing at offset 051Ch")

    patched = bytearray(source)
    patched[PATCH_OFFSET] = 0x08
    if digest(patched) != PATCHED_SHA256:
        raise SystemExit("error: patched output verification failed")

    args.destination.write_bytes(patched)
    print(f"created: {args.destination}")
    print(f"SHA-256: {PATCHED_SHA256.upper()}")


if __name__ == "__main__":
    main()

