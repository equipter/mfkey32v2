#!/usr/bin/python
# Dependencies: https://github.com/equipter/mfkey32v2
# Author: rs-develop (https://github.com/rs-develop/flipper-stuff-pub)
# Version: 2.1
# -----------------------------------------------------------------------

import sys
import re
import subprocess
import os
import time
import serial
import argparse

# Flipper Zero USB CDC CLI uses 230400. Using 9600 can partially work for
# reads but often corrupts multi-step storage write sequences (e.g. leave
# mf_classic_dict_user.nfc empty after remove+write).
FLIPPER_CLI_BAUD = 230400

# -----------------------------------------------------------------------

class MifareExtracterMfkey32v2Error(Exception):
    def __init__(self):
        self.msg = "[!] Error: Could not find \"mfkey32v2\". Get it from \"https://github.com/equipter/mfkey32v2\". Place it in the same dir as the script."
    def __str__(self) -> str:
        return self.msg
class MifareExtracterFlipperDeviceError(Exception):
    def __init__(self):
        self.msg = "[!] Error: Could not find the Flipper Zero device. Make sure it is connected via USB (qFlipper closed), then try again. macOS: ls /dev/cu.* | grep -i flip"
    def __str__(self) -> str:
        return self.msg
class MifareExtracterFlipperCLIError(Exception):
    def __init__(self, what):
        self.msg = "[!] Error: Could not connect to flipper CLI: " + what
    def __str__(self) -> str:
        return self.msg
class MifareExtracterNothingToRead(Exception):
    def __init__(self):
        self.msg = "[+] Info: There is no data to process."
    def __str__(self) -> str:
        return self.msg
class MifareExtracterFileReadError(Exception):
    def __init__(self, what):
        self.msg = "[!] Error: Could not read file \"" + what + "\". Check if the file is available."
    def __str__(self) -> str:
        return self.msg
class MifareExtracterWindowsError(Exception):
    def __init__(self):
        self.msg = "[!] Error: CLI / --detect modes not supported on Windows yet. Use --extract with a log file copied via qFlipper, or the web tool at https://lab.flipper.net/nfc-tools ."
    def __str__(self) -> str:
        return self.msg
class MifareExtracterUnknownError(Exception):
    def __init__(self):
        self.msg = "[!] Unknown error. Create an issue on github."
    def __str__(self) -> str:
        return self.msg

# -----------------------------------------------------------------------

class MifareExtracter:
    
    _flipper_cli = None
    _keys        = set()
    _data        = []

    def __init__(self) -> None:
        # Check for mfkey32v2
        if not os.path.exists("mfkey32v2"):
            raise MifareExtracterMfkey32v2Error()

    def __del__(self) -> None:
        self._disconnectFromFlipperCLI()
        
    def readFile(self, file) -> None:
        try:
            with open(file, "r") as f:
                for line in f:
                    self._data.append(line.encode())
        except:
            raise MifareExtracterFileReadError(file)

    def _detect_flipper_port(self) -> str:
        """Detect and return the serial device basename (e.g. cu.usbmodemflip_xxx or ttyACM0)
        for a connected Flipper Zero. Prefers devices whose name contains 'flip'.

        Supports macOS (primary target), Linux, and basic fallbacks.
        """
        if sys.platform == "darwin":
            # macOS: Flipper usually appears as /dev/cu.usbmodemflip_...
            for glob in ("/dev/cu.usbmodem*", "/dev/cu.*"):
                try:
                    out = subprocess.check_output(
                        ["bash", "-c", f"ls {glob} 2>/dev/null || true"],
                        text=True
                    )
                    candidates = [p.strip() for p in out.strip().splitlines() if p.strip() and os.path.exists(p.strip())]
                    if candidates:
                        # Prefer any that mention flip/flipper
                        for c in candidates:
                            if "flip" in c.lower():
                                return os.path.basename(c)
                        return os.path.basename(candidates[0])
                except Exception:
                    continue
            raise MifareExtracterFlipperDeviceError()
        elif sys.platform.startswith("linux"):
            # Linux: try dmesg (original) then common fallbacks
            try:
                dmesg_res = subprocess.Popen(['dmesg'], stdout=subprocess.PIPE)
                tail_res = subprocess.run(['tail', '-20'], stdin=dmesg_res.stdout, stdout=subprocess.PIPE).stdout.decode('utf-8')
                res = re.findall(r"ttyACM[0-9]{1,2}", tail_res)
                if res:
                    for name in res:
                        if os.path.exists("/dev/" + name):
                            return name
            except Exception:
                pass
            try:
                out = subprocess.check_output(["ls", "/dev/ttyACM*"], stderr=subprocess.DEVNULL, text=True)
                candidates = [os.path.basename(p) for p in out.strip().splitlines() if p.strip()]
                if candidates:
                    return candidates[0]
            except Exception:
                pass
            raise MifareExtracterFlipperDeviceError()
        else:
            if os.name == "nt":
                raise MifareExtracterWindowsError()
            # other POSIX
            try:
                out = subprocess.check_output(["ls", "/dev/ttyUSB*"], stderr=subprocess.DEVNULL, text=True)
                candidates = [os.path.basename(p) for p in out.strip().splitlines() if p.strip()]
                if candidates:
                    return candidates[0]
            except Exception:
                pass
            raise MifareExtracterFlipperDeviceError()

    def _connectToFlipperCli(self) -> None:
        # Connect to flipper
        try:
            port = "/dev/" + self._detect_flipper_port()
            self._flipper_cli = serial.Serial(port=port, baudrate=FLIPPER_CLI_BAUD,
                                              bytesize=8, timeout=2,
                                              stopbits=serial.STOPBITS_ONE)
            if self._flipper_cli:
                time.sleep(0.15)
                self._flipper_cli.reset_input_buffer()
                self._flipper_cli.write(b'\x03\r\n')
                self._flipper_cli.read_until(b'>:')  # skip the CLI welcome screen
                print(f"Connection established. ({port} @ {FLIPPER_CLI_BAUD})")
        except serial.SerialException as s:
            raise MifareExtracterFlipperCLIError(s.strerror)

    def _disconnectFromFlipperCLI(self) -> None:
        if self._flipper_cli:
            try:
                self._flipper_cli.close()
            except serial.SerialException as s:
                raise MifareExtracterFlipperCLIError(s.strerror)

    def _cli_interrupt(self) -> None:
        self._flipper_cli.write(b'\x03')
        time.sleep(0.05)

    def _cli_run(self, command: str, settle: float = 0.05) -> str:
        """Send a CLI command and return the response body up to the next prompt."""
        self._cli_interrupt()
        self._flipper_cli.reset_input_buffer()
        self._flipper_cli.write((command + "\r\n").encode())
        time.sleep(settle)
        raw = self._flipper_cli.read_until(b'>:')
        return raw.decode(errors="replace").replace("\r", "")

    def _read_keys_from_device_file(self, path: str) -> set:
        """Read a newline-separated hex key file from the Flipper and return keys."""
        body = self._cli_run(f"storage read {path}", settle=0.1)
        keys = set()
        if "Storage error" in body:
            return keys
        for item in body.split("\n"):
            item = item.strip()
            res = re.match(r"^[a-fA-F0-9]{12}$", item)
            if res:
                keys.add(res[0].upper())
        return keys

    def _file_size_bytes(self, path: str) -> int:
        body = self._cli_run(f"storage stat {path}")
        m = re.search(r"size:\s*(\d+)b", body, re.I)
        return int(m.group(1)) if m else -1

    def readDataFromFlipper(self) -> None:
        self._connectToFlipperCli()
        body = self._cli_run("storage read /ext/nfc/.mfkey32.log", settle=0.15)
        if "Storage error" in body:
            self._flipper_cli.close()
            raise MifareExtracterFileReadError(".mfkey32.log")
        for item in body.split("\n"):
            item = item.strip()
            if item.startswith("Sec"):
                self._data.append(item.encode())
        print(f"Finished reading \".mfkey32.log\" file. ({len(self._data)} nonce line(s))")

    def writeUserDictToFlipper(self) -> None:
        user_dict = "/ext/nfc/assets/mf_classic_dict_user.nfc"
        user_bkp = "/ext/nfc/assets/mf_classic_dict_user.nfc.bkp"

        # Merge keys already on the device (live dict + backup) so a prior
        # failed write that left the live file empty cannot drop known keys.
        before = set(self._keys)
        for path in (user_dict, user_bkp):
            existing = self._read_keys_from_device_file(path)
            if existing:
                print(f"Merging {len(existing)} key(s) from {path}")
                self._keys |= existing
        print(f"Writing {len(self._keys)} unique key(s) "
              f"({len(self._keys) - len(before)} from device files).")

        if not self._keys:
            print("Warning: no keys to write; leaving user dict unchanged.")
            return

        # Only refresh .bkp from the live file when the live file has content.
        # Never clobber a good backup with an empty source file.
        # Flipper's `storage copy` refuses to overwrite an existing dest, so
        # remove the old .bkp first when refreshing.
        live_size = self._file_size_bytes(user_dict)
        if live_size > 0:
            self._cli_run(f"storage remove {user_bkp}")
            body = self._cli_run(f"storage copy {user_dict} {user_bkp}")
            if "Storage error" in body:
                print("Warning: backup copy to .bkp may have failed (non-fatal)")
            else:
                print(f"Backup updated: {user_bkp}")
        else:
            print("Skipping backup refresh (live user dict empty/missing); keeping existing .bkp")

        # Remove then rewrite with prompt waits between steps.
        self._cli_run(f"storage remove {user_dict}")
        time.sleep(0.05)

        self._cli_interrupt()
        self._flipper_cli.reset_input_buffer()
        # storage write enters interactive mode; end with Ctrl+C after payload.
        self._flipper_cli.write(f"storage write {user_dict}\r\n".encode())
        time.sleep(0.15)
        for key in sorted(self._keys):
            self._flipper_cli.write((key.upper() + "\n").encode())
            time.sleep(0.01)
        self._flipper_cli.write(b'\x03')
        time.sleep(0.1)
        self._flipper_cli.read_until(b'>:')

        # Verify the write landed.
        written = self._read_keys_from_device_file(user_dict)
        size = self._file_size_bytes(user_dict)
        if size <= 0 or not written:
            raise MifareExtracterFlipperCLIError(
                f"user dict write verification failed (size={size}b, keys={len(written)}). "
                "Live dict may be empty; restore from .bkp if needed."
            )
        missing = self._keys - written
        if missing:
            print(f"Warning: {len(missing)} key(s) missing after write verify")
        print(f"The file \"mf_classic_dict_user.nfc\" was written successfully "
              f"({len(written)} key(s), {size}b).")

    def extractKeys(self) -> None:    
        if self._data:
            print("Computing key's ...")
            found = 0
            for line in self._data:
                res = re.findall(r"[a-f0-9]{8}", line.decode().lower())
                if len(res) < 7:
                    continue
                mfkey_res = subprocess.run(['./mfkey32v2', res[0], res[1], res[2], res[3],
                                            res[4], res[5], res[6]],
                                            stdout=subprocess.PIPE).stdout.decode('utf-8')
                key_res = re.findall(r"Found Key: \[([a-f0-9]{12})", mfkey_res)
                if key_res:
                    print(" - Key found: " + key_res[0].upper())
                    self._keys.add(key_res[0].upper())
                    found += 1
            print(" ------------")
            print(f" - {found} crack(s) succeeded this run; {len(self._keys)} unique key(s) in set")
        else:
            raise MifareExtracterNothingToRead()

    def writeUserDict(self) -> None:
        with open("mf_classic_dict_user.nfc", 'w') as out:
            for key in self._keys:
                out.writelines(key.upper() + "\n")
            print("Key's written to mf_classic_dict_user.nfc. Copy the file to your flipper into \"NFC->assets\".")

    def cleanCacheDirectory(self) -> int:
        fileList = []
        if not self._flipper_cli:
            self._connectToFlipperCli()
        # Get file count from /ext/nfc/.cache directory
        self._flipper_cli.write(b'\x03') # send CTR+C (ETX)
        self._flipper_cli.write(f"storage list /ext/nfc/.cache\r\n".encode())
        self._flipper_cli.readline() # skip \r
        self._flipper_cli.readline() # skip >:
        # read file list
        for item in self._flipper_cli.read_until(b'>:').decode().rstrip('\r\n').split('\n'):
            res = re.findall(r"[a-fA-F0-9]{8}.keys", item)
            if res:
                fileList.append(res[0])
        self._flipper_cli.write(b'\x03') # send CTR+C (ETX)
        for file in fileList:
            cmd = "storage remove /ext/nfc/.cache/" + file + "\r\n"
            self._flipper_cli.write(cmd.encode())
            self._flipper_cli.read_until(b'>:')
            self._flipper_cli.write(b'\x03') # send CTR+C (ETX)
        return len(fileList)

    def cleanmfkey32Log(self):
        if not self._flipper_cli:
            self._connectToFlipperCli()
        self._flipper_cli.write(b'\x03') # send CTR+C (ETX)
        self._flipper_cli.write(f"storage remove /ext/nfc/.mfkey32.log\r\n".encode())
        self._flipper_cli.readline() # skip \r
        self._flipper_cli.readline() # skip >:
        for item in self._flipper_cli.read_until(b'>:').decode().rstrip('\r\n').split('\n'):
            if item.startswith("Storage error"):
                raise MifareExtracterFileReadError("File not exists")
        self._flipper_cli.read_until(b'>:')

    def bkpUserDict(self):
        if not self._flipper_cli:
            self._connectToFlipperCli()
        self._flipper_cli.write(b'\x03') # send CTR+C (ETX)
        self._flipper_cli.write(f"storage copy /ext/nfc/assets/mf_classic_dict_user.nfc /ext/nfc/assets/mf_classic_dict_user.nfc.bkp\r\n".encode())
        self._flipper_cli.readline() # skip \r
        self._flipper_cli.readline() # skip >:
        for item in self._flipper_cli.read_until(b'>:').decode().rstrip('\r\n').split('\n'):
            if item.startswith("Storage error"):
                raise MifareExtracterFileReadError("File not exists")
        self._flipper_cli.write(b'\x03') # send CTR+C (ETX)

    def rmUserDict(self):
        if not self._flipper_cli:
            self._connectToFlipperCli()
        self._flipper_cli.write(b'\x03') # send CTR+C (ETX)
        self._flipper_cli.write(f"storage remove /ext/nfc/assets/mf_classic_dict_user.nfc\r\n".encode())
        self._flipper_cli.readline() # skip \r
        self._flipper_cli.readline() # skip >:
        for item in self._flipper_cli.read_until(b'>:').decode().rstrip('\r\n').split('\n'):
            if item.startswith("Storage error"):
                raise MifareExtracterFileReadError("File not exists")
        self._flipper_cli.read_until(b'>:')
        self._flipper_cli.write(b'\x03') # send CTR+C (ETX)

# end class MifareExtracter

# -----------------------------------------------------------------------

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Extracts Mifare values from flipper or a local mfkey32.log file, computes the key's using mfkey32v2 and uploads them to flipper. The new computed key's will added to the content of the \"/SD/nfc/assets/mf_classic_dict_user.nfc\" file. CLI and --detect modes use USB serial (macOS and Linux supported).")
    parser.add_argument("--cli", action='store_true', help="Extract the values via flipper CLI, compute the key's and upload them to flipper (full auto mode)")
    parser.add_argument("--detect", action='store_true',help="Detect Flipper Zero Device - prints only the block device")
    parser.add_argument("--extract", dest="logfile", help="Extract Keys from a local mfkey32.log file and creates a \"mf_classic_dict_user.nfc\" file.", type=str)
    parser.add_argument("--clean-cache", action='store_true',help="Removes all files in the (/SD/nfc/.cache) directory.")
    parser.add_argument("--clean-mfkey32-log", action='store_true',help="Cleans the mfkey32.log file from flipper.")
    parser.add_argument("--bkp-user-dict", action='store_true',help="Creates a backup of the \"mf_classic_dict_user.nfc\" file. The backup file will be placed in the same dir on the flipper.")
    parser.add_argument("--rm-dict-user", action='store_true',help="Removes the \"mf_classic_dict_user.nfc\" file from the flipper.")

    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    try:
        args = parser.parse_args()
        keyExtrator = MifareExtracter()

        if args.cli:
            print("Starting CLI mode...")
            if os.name == "nt":
                raise MifareExtracterWindowsError()
            keyExtrator.readDataFromFlipper()
            keyExtrator.extractKeys()
            keyExtrator.writeUserDictToFlipper()
            print("Finished")
        elif args.detect:
            print("Detecting flipper Block Device...")
            if os.name == "nt":
                raise MifareExtracterWindowsError()
            print("Flipper Device: /dev/" + keyExtrator._detect_flipper_port())
            sys.exit(0)
        elif args.logfile:
            print("Starting local mode. Extracting key's from \"" + args.logfile + "\"")
            keyExtrator.readFile(args.logfile)
            keyExtrator.extractKeys()
            keyExtrator.writeUserDict()
            print("Finished")
        elif args.clean_cache:
            print("Cleaning .cache directory...")
            print("Removed " + str(keyExtrator.cleanCacheDirectory()) + " file(s) from /SD/nfc/.cache")
            print("Finished")
        elif args.clean_mfkey32_log:
            print("Cleaning \".mfkey32.log\" file ...")
            keyExtrator.cleanmfkey32Log()
            print("\".mfkey32.log\" file removed ...")
            print("Finished")
        elif args.bkp_user_dict:
            print("Backup the \"mf_classic_dict_user.nfc\" file ...")
            keyExtrator.bkpUserDict()
            print("Backup done, file: \"mf_classic_dict_user.nfc.bkp\"")
            print("Finished")
        elif args.rm_dict_user:
            print("Removing \"mf_classic_dict_user.nfc\" file from flipper ...")
            keyExtrator.rmUserDict()
            print("User dict removed.")
            print("Finished")
        else:
            raise MifareExtracterUnknownError()

    except Exception as e:
        print(e)

# -----------------------------------------------------------------------