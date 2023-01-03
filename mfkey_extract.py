#!/usr/bin/python
# Dependencies: https://github.com/equipter/mfkey32v2
# Author: rs-develop (https://github.com/rs-develop/flipper-stuff-pub)
# Version: 2.1
# -----------------------------------------------------------------------

import sys
import re
import subprocess
import os
import serial
import argparse

# -----------------------------------------------------------------------

class MifareExtracterMfkey32v2Error(Exception):
    def __init__(self):
        self.msg = "[!] Error: Could not find \"mfkey32v2\". Get it from \"https://github.com/equipter/mfkey32v2\". Place it in the same dir as the script."
    def __str__(self) -> str:
        return self.msg
class MifareExtracterFlipperDeviceError(Exception):
    def __init__(self):
        self.msg = "[!] Error: Could not find the flipper device. Try reconnect it. Close the qFlipper application."
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
        self.msg = "[!] Error: CLI is not supported for Windows jet. Use the extract argument."
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

    def detectFlipperLinux(self) -> str:
        # detect flipper device for linux
        dmesg_res = subprocess.Popen(['dmesg'], stdout=subprocess.PIPE)
        tail_res = subprocess.run(['tail', '-20'], stdin=dmesg_res.stdout, stdout=subprocess.PIPE).stdout.decode('utf-8')
        res = re.findall(r"ttyACM[0-9]{1,2}", tail_res)
        if not res:
            raise MifareExtracterFlipperDeviceError()
        if not os.path.exists("/dev/" + res[0]):
            raise MifareExtracterFlipperDeviceError()
        return res[-1]

    def _connectToFlipperCli(self) -> None:
        # Connect to flipper
        try:
            self._flipper_cli = serial.Serial(port="/dev/" + self.detectFlipperLinux(), baudrate=9600,
                                              bytesize=8, timeout=1, 
                                              stopbits=serial.STOPBITS_ONE)
            if self._flipper_cli:
                self._flipper_cli.read_until(b'>:') # skip the CLI welcom screen
                print("Connection established.")
        except serial.SerialException as s:
            raise MifareExtracterFlipperCLIError(s.strerror)

    def _disconnectFromFlipperCLI(self) -> None:
        if self._flipper_cli:
            try:
                self._flipper_cli.close()
            except serial.SerialException as s:
                raise MifareExtracterFlipperCLIError(s.strerror)

    def readDataFromFlipper(self) -> None:
        self._connectToFlipperCli()
        self._flipper_cli.write(b'\x03') # send CTR+C (ETX)
        self._flipper_cli.write(f"storage read /ext/nfc/.mfkey32.log\r\n".encode())
        self._flipper_cli.readline() # skip \r\n
        self._flipper_cli.readline() # skip >:
        print(self._flipper_cli.readline()) # skip size
        for item in self._flipper_cli.read_until(b'>:').decode().rstrip('\r\n').split('\n'):
            if item.startswith("Storage error"):
                self._flipper_cli.close()
                raise MifareExtracterFileReadError(".mfkey32.log")
            if item.startswith("Sec"):
                self._data.append(item.encode())
        self._flipper_cli.write(b'\x03') # send CTR+C (ETX)
        print("Finished reading \".mfkey32.log\" file.")

    def writeUserDictToFlipper(self) -> None:
        self._flipper_cli.write(b'\x03') # send CTR+C (ETX)
        self._flipper_cli.write(f"storage read /ext/nfc/assets/mf_classic_dict_user.nfc\r\n".encode())
        print(self._flipper_cli.readline()) # skip \r
        print(self._flipper_cli.readline()) # skip >:
        print(self._flipper_cli.readline()) # skipt cmd
        # read the old key's from mf_classic_dict_user.nfc
        for item in self._flipper_cli.read_until(b'>:').decode().rstrip('\r\n').rstrip('\r').split('\n'):
            if not item.startswith("Storage error"):
                res = re.match(r"^[a-fA-F0-9]{12}", item)
                if res:
                    self._keys.add(res[0].upper())
        # after reading, remove the old file
        self._flipper_cli.write(f"storage remove /ext/nfc/assets/mf_classic_dict_user.nfc\r\n".encode())
        self._flipper_cli.write(b'\x03') # send CTR+C (ETX)
        self._flipper_cli.write(f"storage write /ext/nfc/assets/mf_classic_dict_user.nfc\r".encode())
        for key in self._keys:
            self._flipper_cli.write((key.upper()+'\r\n').encode())
        self._flipper_cli.write(b'\x03') # stop flipper writing data by sending CTR+C (ETX)
        print("The file \"mf_classic_dict_user.nfc\" was written to flipper successfully.")

    def extractKeys(self) -> None:    
        if self._data:
            print("Computing key's ...")
            for line in self._data:
                res = re.findall(r"[a-f0-9]{8}", line.decode())
                mfkey_res = subprocess.run(['./mfkey32v2',res[0],res[1], res[2], res[3], 
                                            res[4], res[5], res[6]], 
                                            stdout=subprocess.PIPE).stdout.decode('utf-8')
                key_res = re.findall(r"Found Key: \[([a-f0-9]{12})", mfkey_res)
                if key_res:
                    print(" - Key found: "+ key_res[0].upper())
                    self._keys.add(key_res[0].upper())
            print(" ------------")
            print(" - " + str(len(self._keys)) + " unique key's found!")
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
    parser = argparse.ArgumentParser(description = "Extracts Mifare valus from flipper or a local mfkey32.log file, computes the key's using mfkey32v2 and uploads them to flipper. The new computed key's will added to the content of the \"/SD/nfc/assets/mf_classic_dict_user.nfc\" file. The cli and detect mode are Linux only.")
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
            print("Flipper Device: /dev/" + keyExtrator.detectFlipperLinux())
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