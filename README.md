

# Mfkey32 Version 2
Mfkey32v2 is a tool used to calculate Mifare Classic Keys from encrypted nonces obtained from the reader. 

**Note: Nonce in computer terminology means "Number used once"**


## Acknowledgements

 - [Mfkey Base Code](https://github.com/rfidresearchgroup/proxmark3)
 - [RRG Author's file](https://github.com/equipter/mfkey32v2/blob/main/AUTHORS.md)
 - [Bettse for assisting in development](https://gitlab.com/bettse)

| [Github](https://github.com/equipter) | [Twitter](https://twitter.com/Equip0x80) | [Reddit](https://www.reddit.com/user/equipter) | equip paypal: equipter@outlook.com | bettse paypal: bettse@fastmail.fm | [Discord](https://discord.gg/e9XzfG5nV5) |
| :---: | :---: | :---: | :---: | :---: | :---: |

## Disclaimer

**No one involved in this project is responsible for how you use it. Always follow local laws and EULAs.**

## What is Mfkey32v2
Mfkey32v2 calculates Mifare Classic Sector keys from encrypted nonces collected by emulating the initial card and recording the interaction between the emulated card and the respective reader. 

While performing authentication, the reader will send "nonces" to the card which can be decrypted into keys. 

**Mfkey32v2 is not magic it cannot create you a working credential without an initial card. The Keys generated are not keys to open the door, they are keys to unlock and read sectors from inside the card itself.**

##  Mfkey32v2 Implementations 
MfKey32v2 has a few different implementations as time has progressed.

From the list below select the mfkey32v2 instructions best suited to you. 

* [Generic Standalone Mfkey32v2 Cli usage instructions](https://github.com/equipter/mfkey32v2/blob/main/Docs/Generic.md)
* [FlipperZero Mfkey32v2 Cli instructions](https://github.com/equipter/mfkey32v2/blob/main/Docs/Flippercli.md)
* [FlipperZero Mfkey32v2 Web App Instructions](https://github.com/equipter/mfkey32v2/blob/main/Docs/flip-site.md)
* [FlipperZero Mfkey32v2 Mobile companion app Instructions](https://github.com/equipter/mfkey32v2/blob/main/Docs/flip-app.md)

### Datasheets
If you are interested in mfkey32v2 and/or mifare classic as a whole, below are links for mifare classic and other relevant datasheets.
* [Mifare Classic 1k ev1](https://www.nxp.com/docs/en/data-sheet/MF1S50YYX_V1.pdf)
* [Mifare Classic 4k ev1](https://www.nxp.com/docs/en/data-sheet/MF1S70YYX_V1.pdf)
* [Mifare Identifcation Procedure - AN10833](https://www.nxp.com/docs/en/application-note/AN10833.pdf)

## mfkey_extract - automate the calculation process with flipper zero
Automatically downloads the content of the `.mfkey32.log` file from the flipper, reads the values, calculates the key's using `mfkey32v2` and uploads the key's to the flippers nfc user dict. Also provides the extrcat mode. This mode can be used to extract the key's from a local `.mfkey32.log` file which was downloaded using qFlipper. The extract mode creates a `mf_classic_dict_user.nfc` file which can be uploaded to the flipper device using qFlipper. The `cli` mode is for Linux users only. `Mfkey32vs` is mandatory (https://github.com/equipter/mfkey32v2). 

**Available arguments**
```shell
usage: mfkey_extract.py [-h] [--cli] [--detect] [--extract LOGFILE]

Extracts Mifare valus from flipper or a local mfkey32.log file, computes the
key's using mfkey32v2 and uploads them to flipper. The cli and detect mode are
Linux only.

options:
  -h, --help         show this help message and exit
  --cli              Extract the values via flipper CLI, compute the key's and
                     upload them to flipper (full auto mode)
  --detect           Detect Flipper Zero Device - prints only the block device
  --extract LOGFILE  Extract Keys from a local mfkey32.log file and creates a
                     "mf_classic_dict_user.nfc" file.
```

**Steps for cli mode**
1) Read the Mifare Classic Card/Chip
2) Skip reading the key`s
3) Select "Detect Reader"
4) Connect the flipper to the computer
5) run `mfkey_extract.py --cli`
6) Read the card again. Now more key's and sectors should be available for read.

**Steps for extract mode**
1) Read the MIFARE Classic Card/Chip
2) Skip reading the key's
3) Select "Detect Reader"
4) Extract the '.mfkey32.log' using qFlipper (enable hidden files)
5) Execute the script: `mfkey_extract.py --extract` </path/to/mfkey32.log>'
6) Copy the generated 'mf_classic_dict_user.nfc' to the flipper (maybe backup your old one first)
7) Read the card again.

# Support 
For support in using Mfkey32v2 message Equip#1515 on discord, submit a github issue or join my [discord](https://discord.gg/e9XzfG5nV5).
