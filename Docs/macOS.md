# macOS Usage (mfkey32v2 + Flipper)

These instructions are specific to macOS + the improved cross-platform support in this fork.

## Quick Requirements (use brew)

```bash
# For building the C cracker
xcode-select --install   # or brew install gcc make

# Python serial support (required for the auto CLI mode)
python3 -m pip install pyserial

# Optional but handy for manual CLI inspection
brew install minicom
```

## Build the cracker

```bash
git clone https://github.com/equipter/mfkey32v2 /path/to/mfkey32v2
cd /path/to/mfkey32v2
make mfkey32v2
ls -l mfkey32v2   # should exist and be executable
```

## Finding your Flipper on macOS

With the Flipper plugged in via USB-C and **qFlipper closed**:

```bash
ls /dev/cu.*
# or more specific
ls /dev/cu.usbmodem* | cat
```

You should see something like `/dev/cu.usbmodemflip_YourName` or similar.

The updated `mfkey_extract.py` now auto-detects this (prefers names containing "flip").

Manual serial (if you want to inspect):

```bash
screen /dev/cu.usbmodemflip_YourName
# or
minicom -D /dev/cu.usbmodemflip_YourName
```

Inside the CLI you can run `storage list /ext/nfc` etc. Exit screen with Ctrl-A then K, confirm with Y.

## Full auto flow (recommended once set up)

1. On the Flipper: NFC → Saved → [your card] → Detect Reader (or Extract MF Keys). Hold to the reader to collect nonces. A `.mfkey32.log` file will appear on the SD (hidden).

2. Connect Flipper to your Mac, close qFlipper.

3. In the mfkey32v2 directory (where the binary lives):

   Simplest:
   ```bash
   ./flipper-crack
   ```

   Or manually:
   ```bash
   python3 mfkey_extract.py --cli
   ```

   (You can also `make flipper-crack`.)

   This will:
   - Auto-detect the serial port
   - Pull the nonce log from `/ext/nfc/.mfkey32.log`
   - Run the cracker for each entry
   - Read your existing user dict, merge the new keys
   - Create a `.bkp` of the old user dict on the device
   - Write the merged dict back to `/ext/nfc/assets/mf_classic_dict_user.nfc`

4. On the Flipper (after the script finishes):
   - Go to NFC → clear the cache if needed (delete files under `/ext/nfc/.cache` via qFlipper or `storage remove` in CLI)
   - Re-read your original saved card file. You should now find more sectors.

## Manual / qFlipper path (very reliable)

- Open qFlipper → File manager.
- Enable "Show hidden files" (check the app settings or view options).
- Navigate to `/ext/nfc/` and download `.mfkey32.log` (the dot makes it hidden).
- Run locally:
  ```bash
  python3 mfkey_extract.py --extract /path/to/downloaded/.mfkey32.log
  ```
  This produces a `mf_classic_dict_user.nfc` in the current directory containing the new keys.
- (Optional but recommended) First download your current `/ext/nfc/assets/mf_classic_dict_user.nfc` as a backup.
- Upload the generated `mf_classic_dict_user.nfc` (or the merged one) back to `/ext/nfc/assets/mf_classic_dict_user.nfc` via qFlipper.
- Clear cache + re-read the card on the device.

## Web / zero-compile path

If you don't want to build anything locally:

1. Collect nonces on the Flipper (Detect Reader).
2. In Chrome/Edge: go to https://lab.flipper.net/nfc-tools
3. Connect your Flipper (Web Serial).
4. Use the "GIVE ME THE KEYS" / Mfkey tool.

**Warning**: The web tool often replaces (rather than merges into) your `mf_classic_dict_user.nfc`. Download a backup of your user dict first using qFlipper or the CLI `storage read` command.

## Other notes

- The script also supports `--bkp-user-dict`, `--clean-cache`, `--clean-mfkey32-log`, `--rm-dict-user` etc. for maintenance.
- `--detect` will print the port it would use.
- For the generic (non-Flipper) CLI usage see `Docs/Generic.md`.
- Original Flipper-focused docs: `Docs/Flippercli.md`

After any key update, power-cycle the Flipper or at least clear the NFC cache for the changes to take full effect on the next read.

Support: see the main README or the original repo issues/Discord pointers.

## Verification performed in this fork (on macOS)

- `make mfkey32v2` succeeds and produces a working binary.
- Example from README:
  `./mfkey32v2 2a234f80 240bd022 ad2e1687 57e6f7e4 18a4bd3e accc1a23 6f10e401`
  correctly outputs `Found Key: [a0a1a2a3a4a5]`.
- `python3 mfkey_extract.py --help` shows the updated macOS-aware description.
- `python3 mfkey_extract.py --detect` (and the new `_detect_flipper_port`) successfully located a real device: `/dev/cu.usbmodemflip_Kuch1n01`.
- The `flipper-crack` wrapper and `make flipper-crack` target exist and are executable.

When you have nonces collected, you can now safely run the full flow. The script will respect the exact paths `/ext/nfc/.mfkey32.log` (read) and `/ext/nfc/assets/mf_classic_dict_user.nfc` (read + backup + write merged keys).
