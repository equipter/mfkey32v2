# Mfkey32v2
*base code credits to rfidresearchgroup [link](https://github.com/rfidresearchgroup/proxmark3)*

*big shoutout to bettse for assisting in development*
| ![GitHub followers](https://img.shields.io/github/followers/equipter?label=Equipter%20&logo=GitHub&style=flat-square) | ![Twitter Follow](https://img.shields.io/twitter/follow/equip0x80?color=b9d1ff&label=Equip0x80&logo=Twitter&style=flat-square) | ![Subreddit subscribers](https://img.shields.io/reddit/subreddit-subscribers/rfid?logo=reddit&logoColor=ffffff&style=flat-square) | equip paypal: equipter@outlook.com | bettse paypal: bettse@fastmail.fm |
| :---: | :---: | :---: | :---: | :---: |

Mfkey32v2 extracts keys from nonces collected during the authentication process. these nonces can be collected by emulating the credential to allow the reader to begin despensing the necessary information to begin extraction. 

## Requirements 
`GCC for compiling C`
`For compiling on windows you'll need a C compiler or use MINGW to create a virtual environment to use GCC`

## Compilation 
1. Before compiling make sure your gcc is up to date 
2. Download code
3. Navigate into repo directory 
4. Compile with `gcc mfkey32v2.c crypto1/crypto1.c crypto1/crypto01.c crypto1/bucketsort.c -o mfkey32v2 -Iinclude`

now that youve compiled youre ready to use!

## Usage
command syntax for mfkey32v2 is `./mfkey32v2 <uid> <nt> <nr_0> <ar_0> <nt1> <nr_1> <ar_1>`

if you've come from the flipper mfkey32v2 logging, instructions for your command structuring is below:
if you arent comfortable or capable of running mfkey32v2 by yourself. Message your log output to bettse or equip on discord. 

1. On your FZ navigate to settings an enable debug. 
2. Then on log level, adjust to `Debug` 
3. Scan your Mifare Classic and begin `read mifare classic` special action
(NOTE: you do not need to have found any keys you just need have a base .nfc file from the output)
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
9. run ./mfkey32v2 with parameters like such 
`./mfkey32v2 [uid] [topline log] [bottomline log]`
example: UID 939be0d5 
```
70795 [D][MfClassic]: 939be0d5 keyA block 3 nt/nr/ar: 4e70d691 b3a576be 02c1559b
...
77521 [D][MfClassic]: 939be0d5 keyA block 3 nt/nr/ar: c6efb126 d24dd966 03fc7386
```
your command should look like this:
`./mfkey32v2 939be0d5 4e70d691 b3a576be 02c1559b c6efb126 d24dd966 03fc7386`
your key should be popped out like so 
`Found Key: [a0a1a2a3a4a5]`

ta da! your keyA for block3 is: `a0a1a2a3a4a5`
