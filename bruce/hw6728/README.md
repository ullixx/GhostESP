# Bruce build for HW6728 ESP32-S3 N16R8

This folder contains only the HW6728 board overlay. The Bruce firmware itself is
kept as an independent AGPL-3.0 Git submodule at `third_party/bruce-firmware`.
GhostESP remains a separate firmware and is not modified by this build.

## Hardware profile

- ESP32-S3
- 16 MB flash
- 8 MB octal PSRAM (`qio_opi`, `BOARD_HAS_PSRAM=1`)
- LittleFS on the internal flash
- Dummy display backend (the HW6728 has no display)
- Bruce BLE serial API enabled automatically at boot for Bruce Remote

No RF/NFC/IR peripherals or GPIO pin assignments are enabled by default. Add
board-specific pins only after verifying the HW6728 schematic/pinout.

## Build

The board interface includes `globals.h` so the Bruce configuration object is declared during compilation.

From the GhostESP repository root, with submodules initialized:

```sh
git submodule update --init --recursive
python3 scripts/prepare_bruce_hw6728.py
cd third_party/bruce-firmware
pio run -e hw6728-n16r8
```

The GitHub Actions workflow `.github/workflows/build-bruce-hw6728.yml` performs
the same preparation and build, then uploads the firmware artifact.

## Bruce Remote on iPhone

Use the separate upstream app: https://github.com/BruceDevices/App-IOS

The app requires iOS 17+ and Xcode 16+ to build/sign. The firmware advertises the
Bruce BLE serial service at boot. The iOS app can use device status, terminal,
modules supported by firmware, and filesystem operations.

**Display limitation:** this HW6728 board has no screen. The app's live screen
mirror/D-pad feature depends on Bruce display draw calls, so it cannot provide a
normal mirrored menu on this board. BLE terminal and supported command-based
features are the intended control path.

The iPhone app does not flash firmware over USB; flashing still requires a
computer with a compatible USB flashing workflow.

## Storage partition

The 16 MB partition table reserves a large app slot and an internal LittleFS
partition. The partition subtype remains `spiffs`, as required by the ESP32
Arduino LittleFS partition discovery; the partition label is `littlefs`.
