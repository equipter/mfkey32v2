
# Mfkey32 v2


| ![GitHub followers](https://img.shields.io/github/followers/equipter?label=Equipter%20&logo=GitHub&style=flat-square) | ![Twitter Follow](https://img.shields.io/twitter/follow/equip0x80?color=b9d1ff&label=Equip0x80&logo=Twitter&style=flat-square) | ![Subreddit subscribers](https://img.shields.io/reddit/subreddit-subscribers/rfid?logo=reddit&logoColor=ffffff&style=flat-square) | equip paypal: equipter@outlook.com | bettse paypal: bettse@fastmail.fm | [Discord](https://discord.gg/e9XzfG5nV5) |
| :---: | :---: | :---: | :---: | :---: | :---: |

Mfkey32v2 extracts keys from nonces collected during the authentication process. These nonces can be collected by emulating the credential to allow the reader to begin despensing the necessary information to begin extraction.
## Acknowledgements

 - [Mfkey Base Code](https://github.com/rfidresearchgroup/proxmark3)
 - [Bettse for assisting in development](https://gitlab.com/bettse)



## Requirements 
GCC for compiling C (deb)
make for utilising the makefile. build-essential contains both of these for you to use
- `sudo apt install build-essential`


(For compiling on windows you'll need a C compiler or use MINGW to create a virtual environment to use GCC)

## Compilation 
1. Before compiling make sure your gcc is present and  up to date 
2. Download code
- `git clone https://github.com/equipter/mfkey32v2`
3. Navigate into repo directory 
- `cd mfkey32v2/`
4. Compile code with make
- `make mfkey32v2`

(if make is for some reason non cooperative you can manually compile with gcc using this command `gcc mfkey32v2.c include/crypto1.c include/crypto01.c include/bucketsort.c -o mfkey32v2 -Iinclude`


## Standalone Usage

command syntax for mfkey32v2 is `./mfkey32v2 <uid> <nt> <nr_0> <ar_0> <nt1> <nr_1> <ar_1>`

## FlipperZero Usage/Examples
if you've come from the flipper mfkey32v2 logging, instructions for your command structuring is below:
if you arent comfortable or capable of running mfkey32v2 by yourself. Message your log output to bettse or equip on discord. 

1. On your FZ navigate to settings an enable debug. 
2. Then on log level, adjust to `Debug` 
3. Scan your Mifare Classic and begin `read mifare classic` special action
**(NOTE: you do not need to have found any keys you just need have a base .nfc file from the output)**
4. Save your credential on the flipper and begin the card emulation
5. open your Flipper CLI 
[instructions for CLI](https://forum.flipperzero.one/t/cli-command-line-interface-examples/1874) 
link to [webcli](https://my.flipp.dev/)
6. start `log` 
7. while still emulating the UID, approach your flipperzero to the reader 
8. your CLI should output logs see below for an example. find the lines like this 
```
70795 [D][MfClassic]: 939be0d5 keyA block 3 nt/nr/ar: 4e70d691 b3a576be 02c1559b
77521 [D][MfClassic]: 939be0d5 keyA block 3 nt/nr/ar: c6efb126 d24dd966 03fc7386
```
now, on your external device where you have downloaded and compiled mfkey32v2 

run `./mfkey32v2` with parameters like such 
`./mfkey32v2 [uid] [topline log] [bottomline log]`

example: UID 939be0d5 

your command should look like this:
`./mfkey32v2 939be0d5 4e70d691 b3a576be 02c1559b c6efb126 d24dd966 03fc7386`

your key should be output out like so 
`Found Key: [a0a1a2a3a4a5]`

your keyA for Block 3/sector 1 is: `a0a1a2a3a4a5`

## Used By

This project is used by the following Repositories:

- [FlipperZero Offical firmware](https://github.com/flipperdevices/flipperzero-firmware)
- [RogueMaster FlipperZero Firmware](https://github.com/RogueMaster/flipperzero-firmware-wPlugins)
- [Credited in DJsime Awesome-Flipperzero](https://github.com/djsime1/awesome-flipperzero/blob/main/Firmwares.md)


## Support

For support, Message Equip on discord Equip#1515 or join The discord server [Link](https://discord.gg/e9XzfG5nV5)

