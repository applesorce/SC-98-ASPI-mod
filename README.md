# SC-98-ASPI-MOD

A one-byte patch for I-O DATA `ASPISC98.SYS` Ver.1.06 that enables SCSI selection with ATN on the I-O DATA SC-98 for NEC PC-98 computers.

It allows devices with multiple logical units under a single SCSI ID, such as the I-O DATA DATASTATION DTST-H640, to select each LUN correctly.

## What it changes

The original ASPI manager executes SCSI commands through SC-98 BIOS function `AH=09h`:

```text
Select without ATN and Transfer
```

The patch changes it to function `AH=08h`:

```text
Select with ATN and Transfer
```

This enables the SCSI IDENTIFY message used to select the requested LUN.

Only one byte is changed at file offset `0x051C`:

```text
Original: 09
Patched:  08
```

## Supported file

The patch only supports this exact driver:

```text
Filename:  ASPISC98.SYS
Version:   1.06
Size:      4355 bytes
SHA-256:   4F016E4014141AE661AA787490B62EB8038456B2AEF3AC36542C52118296C62F
```

Patched output:

```text
Size:      4355 bytes
SHA-256:   CD0D2C90AC659393BE05F8493446896B93773F046D0FCD4A1ADA8AC5669F85F6
```

Do not apply the patch to a file with a different size or SHA-256 hash.

## How to apply

Apply `patches/ASPISC98-ATN.IPS` to the original `ASPISC98.SYS` with an IPS-compatible patching tool.

Keep the original driver and save the patched file under a different name, for example:

```text
ASPISC8.SYS
```

If the Python patching tool is included, it can be used instead:

```console
python tools/apply_patch.py ASPISC98.SYS ASPISC8.SYS
```

## How to use

Load the patched ASPI manager before the ASPI disk driver in `CONFIG.SYS`:

```dos
DEVICEHIGH=A:\TEST\ASPISC8.SYS
DEVICEHIGH=A:\BIN\MO\MODISK.SYS /ASPI /LUN
```

Change the paths to match the locations on your system.

Do not load the original `ASPISC98.SYS` and patched `ASPISC8.SYS` at the same time.

`MODISK.SYS` Ver.1.40 does not require modification. Its `/ASPI /LUN` options scan LUN 0 through 7 and register supported removable devices separately.

Confirmed on a DATASTATION DTST-H640: MOUTL detects both LUN 0 and LUN 1 with the `ASPI LUN` options, and the ATA card on LUN 1 can be formatted and accessed normally.

## Notes

- The modification affects all SCSI commands sent through this ASPI manager.
- Compatibility with other SCSI devices is not guaranteed.
- Keep the original driver and a bootable recovery disk before installing the patched version.
- The original I-O DATA driver is copyrighted software and is not included in this repository.
