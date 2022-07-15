# Mfkey32v2
*base code credits to rfidresearchgroup [link](https://github.com/rfidresearchgroup/proxmark3)*

*big shoutout to bettse for assisting in development*
| ![GitHub followers](https://img.shields.io/github/followers/equipter?label=Equipter%20&logo=GitHub&style=flat-square) | ![Twitter Follow](https://img.shields.io/twitter/follow/equip0x80?color=b9d1ff&label=Equip0x80&logo=Twitter&style=flat-square) | ![Subreddit subscribers](https://img.shields.io/reddit/subreddit-subscribers/rfid?logo=reddit&logoColor=ffffff&style=flat-square) | equip paypal: equipter@outlook.com | bettse paypal: bettse@fastmail.fm |
| :---: | :---: | :---: | :---: | :---: |


Calculates sector keys from nonces. 

## Compilation 
1. Before compiling make sure your gcc is up to date 
2. Download code
3. Navigate into repo directory 
4. Compile chosen mfkey
* mfkey32v2: `gcc mfkey32v2.c crypto1/crypto1.c crypto1/crypto01.c crypto1/bucketsort.c -o mfkey32v2 -Iinclude`
* mfkey32: `gcc mfkey32.c crypto1/crypto1.c crypto1/crypto01.c crypto1/bucketsort.c -o mfkey32 -Iinclude`
* mfkey64: `gcc mfkey64.c crypto1/crypto1.c crypto1/crypto01.c crypto1/bucketsort.c -o mfkey64 -Iinclude`

now that youve compiled youre ready to use!

## Usage

Mfkey32v2 works by two partial authentications.
command syntax for mfkey32v2 is `./mfkey32v2 <uid> <nt> <nr_0> <ar_0> <nt1> <nr_1> <ar_1>`
example: UID `939be0d5`
syntax: `./mfkey32v2 939be0d5 4e70d691 b3a576be 02c1559b c6efb126 d24dd966 03fc7386`
mfkey32v2 works by using an alternative method for nonce cracking

Mfkey32 works by two 32 bits of keystream authentication.
command syntax for mfkey32 is `./mfkey32 <uid> <nt> <nr_0> <ar_0> <nr_1> <ar_1>`


Mfkey64 works on one complete authentication.
command syntax for mfkey64 is `./mfkey64 <uid> <nt> <{nr}> <{ar}> <{at}> [enc...]`
