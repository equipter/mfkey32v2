

# Mfkey32 Version 2

Mfkey32v2 extracts mifare classic keys from nonces collected during the authentication process. These nonces can be collected by emulating the credential to allow the reader to begin despensing the necessary information to begin extraction.
## Acknowledgements

 - [Mfkey Base Code](https://github.com/rfidresearchgroup/proxmark3)
 - [Bettse for assisting in development](https://gitlab.com/bettse)

| [Github](https://github.com/equipter) | [Twitter](https://twitter.com/Equip0x80) | [Reddit](https://www.reddit.com/user/equipter) | equip paypal: equipter@outlook.com | bettse paypal: bettse@fastmail.fm | [Discord](https://discord.gg/e9XzfG5nV5) |
| :---: | :---: | :---: | :---: | :---: | :---: |


## Requirements 

1. GCC for compiling C (deb)
2. make for utilising the makefile.
3. git for cloning the repo 

GCC and Makefile
`sudo apt install build-essential`

git - github CLI 
`sudo apt-get install git`

**For compilation and use on windows you will need to use MingW or alternate virtual environment.** [link to mingW install instructions](https://genome.sph.umich.edu/wiki/Installing_MinGW_%26_MSYS_on_Windows)



## Compilation 
1. Download code
- `git clone https://github.com/equipter/mfkey32v2`
2. Navigate into repo directory 
- `cd mfkey32v2/`
3. Compile mfkey32v2
- `make mfkey32v2`

### Compiling On Windows
If `mingw32-make` fails with the error `make (e=2): The system cannot find the file specified.` try: `mingw32-make CC=gcc`

## Standalone Usage

command syntax for mfkey32v2 is `./mfkey32v2 <uid> <nt> <nr_0> <ar_0> <nt1> <nr_1> <ar_1>`

## FlipperZero Usage/Examples


### Using Detect Reader

Another example is the usage of the flippers Detect Reader function. Simply activate detect reader and approach the reader you wish to obtain keys from. After a moment a file will be output in the nfc folder with the suffix `.mfkey.log`, inside this file there are log lines of which you can use to calculate the keys using mfkey32v2. 


Example:
```
Sector 0 key A cuid 2a234f80 nt0 240bd022 nr0 ad2e1687 ar0 57e6f7e4 nt1 18a4bd3e nr1 accc1a23 ar1 6f10e401
Sector 0 key A cuid 2a234f80 nt0 a5b5d569 nr0 30e2ff62 ar0 5e1b926d nt1 d2760a5c nr1 6157acb0 ar1 cb0fd13d
Sector 0 key A cuid 2a234f80 nt0 81ee85ad nr0 3290942e ar0 f76b6ec7 nt1 9c95e4ac nr1 d05dc608 ar1 729dcbe9
Sector 0 key A cuid 2a234f80 nt0 b61bf034 nr0 9c04ca8f ar0 787f79ce nt1 01e9294b nr1 22218ef9 ar1 c4e54292
Sector 0 key A cuid 2a234f80 nt0 f793ebf3 nr0 b783530a ar0 d1607737 nt1 a7ed17fe nr1 50d0c65b ar1 4b43383c
...
```

Use the keys one by one as logged in the file. For the first line it will be 
```
./mfkey32v2 2a234f80 240bd022 ad2e1687 57e6f7e4 18a4bd3e accc1a23 6f10e401
```

You can use cut or awk to generate these statements from the log file:
```
# Using cut
IFS=$'\n'; for line in `cut -d' ' -f6,8,10,12,14,16,18 mfkey32.log`; do echo ./mfkey32 $line; done

# Using awk
IFS=$'\n'; for line in `awk '{print $6 " " $8 " " $10 " " $12 " " $14 " " $16" " $18}' mfkey32.log`; do echo ./mfkey32v2 $line; done
```

The output shows the calculated key
```
MfKey32v2 open source Mifare Classic key-recovery tool
Cracks keys by two 32bit keystream authenticationsRecovering key for:
    uid: 2a234f80
   nt_0: 240bd022
 {nr_0}: ad2e1687
 {ar_0}: 57e6f7e4
   nt_1: 18a4bd3e
 {nr_1}: accc1a23
 {ar_1}: 6f10e401

LFSR successors of the tag challenge:
  nt': fdef821e
 nt'': 066a97e6

Keystream used to generate {ar} and {at}:
  ks2: aa0975fa

Found Key: [a0a1a2a3a4a5]
```

and if this method doesnt work you can scrape from the CLI log manually, see below 

### Using Log

if you've come from the flipper mfkey32v2 logging, instructions for your command structuring is below:
if you arent comfortable or capable of running mfkey32v2 by yourself. Message your log output to bettse or equip on discord. 
![](https://i.imgur.com/pYD9qUC.gif)

1. On your FZ navigate to settings an enable debug. 
2. Then on log level, adjust to `Debug` 
3. Scan your Mifare Classic
**(NOTE: you do not need to have found any keys you just need have a base .nfc file from the output)**
4. Save your credential on the flipper and begin the card emulation
5. connect your flipper and open your Flipper CLI 
[instructions for CLI](https://forum.flipperzero.one/t/cli-command-line-interface-examples/1874) 
link to [webcli](https://my.flipp.dev/)
6. start `log` 
7. while still emulating the UID, approach your flipperzero to the reader while your device is still connected to the flipper
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

your keyA for Block 3(sector 0) is: `a0a1a2a3a4a5`


### automatically scrape log file for keys 
if youve used the detect reader method you will be outputted an `mfkey.log`, drag that file into the mfkey32v2 folder and run this command to easily produce the keys for you from the file. 

```
for i in $(cat mfkey.log | cut -d" " -f6,8,10,12,14,16,18 | sed 's/ /,/g'); do cuid=$(echo $i | cut -d"," -f1); v2=$(echo $i | cut -d"," -f2);v3=$(echo $i | cut -d"," -f3);v4=$(echo $i | cut -d"," -f4);v5=$(echo $i | cut -d"," -f5);v6=$(echo $i | cut -d"," -f6);v7=$(echo $i | cut -d"," -f7); ./mfkey32v2 $cuid $v2 $v3 $v4 $v5 $v6 $v7 | fgrep 'Found Key' >> keys.txt; done
```

you can also use the included .sh file, drag your mfkey.log file into the mfkey32v2 folder and run the .sh file to automatically scape keys 


## Used By

This project is used by the following Repositories:

- [Credited on @UberGuidoZ 's playground repo](https://github.com/UberGuidoZ/Flipper)
- [FlipperZero Offical firmware](https://github.com/flipperdevices/flipperzero-firmware)
- [RogueMaster FlipperZero Firmware](https://github.com/RogueMaster/flipperzero-firmware-wPlugins)
- [Credited in DJsime Awesome-Flipperzero](https://github.com/djsime1/awesome-flipperzero/blob/main/Firmwares.md)


## Support

For support, Message Equip on discord Equip#1515 or join The discord server [Link](https://discord.gg/e9XzfG5nV5)

