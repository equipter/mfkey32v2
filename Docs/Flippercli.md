
# Flipper Cli Usage
These instructions are for using the CLI Application in unison with the flipper.

## Requirements 

1. GCC for compiling C (deb)
2. make for utilising the makefile.
3. git for cloning the repo 


GCC and Makefile
`sudo apt install build-essential`

git - github CLI 
`sudo apt-get install git`

**For compilation and use on windows you will need to use MingW or alternate virtual debian environment.** [link to mingW install instructions](https://genome.sph.umich.edu/wiki/Installing_MinGW_%26_MSYS_on_Windows)



## Compilation 
1. Download code
- `git clone https://github.com/equipter/mfkey32v2`
2. Navigate into repo directory 
- `cd mfkey32v2/`
3. Compile mfkey32v2
- `make mfkey32v2`

### Compiling On Windows
If `mingw32-make` fails with the error `make (e=2): The system cannot find the file specified.` 

try: `mingw32-make CC=gcc`

## Collecting the nonces.

### Detect Reader 
In the latest release, you can use detect reader using a saved card. This method is the recommended one because it won't use a fixed UID like normal detect reader uses and also it is more discreet than using a computer connected to your Flipper.



![](https://user-images.githubusercontent.com/45500329/201108244-7dc02b7a-fd82-4446-85e3-c44e852c69b7.gif)

You can use cut or awk to generate these statements from the log file:
```
# Using cut
IFS=$'\n'; for line in `cut -d' ' -f6,8,10,12,14,16,18 mfkey32.log`; do echo ./mfkey32 $line; done
 
# Using awk
IFS=$'\n'; for line in `awk '{print $6 " " $8 " " $10 " " $12 " " $14 " " $16" " $18}' mfkey32.log`; do echo ./mfkey32v2 $line; done
```

### automatically scrape log file for keys 
if youve used the detect reader method you will be outputted an `mfkey.log`, drag that file into the mfkey32v2 folder and run this command to easily produce the keys for you from the file. 
 
```
for i in $(cat mfkey.log | cut -d" " -f6,8,10,12,14,16,18 | sed 's/ /,/g'); do cuid=$(echo $i | cut -d"," -f1); v2=$(echo $i | cut -d"," -f2);v3=$(echo $i | cut -d"," -f3);v4=$(echo $i | cut -d"," -f4);v5=$(echo $i | cut -d"," -f5);v6=$(echo $i | cut -d"," -f6);v7=$(echo $i | cut -d"," -f7); ./mfkey32v2 $cuid $v2 $v3 $v4 $v5 $v6 $v7 | fgrep 'Found Key' >> keys.txt; done
```
 
you can also use the included .sh file, drag your mfkey.log file into the mfkey32v2 folder and run the .sh file to automatically scape keys 


## mfkey_extract - automate the key calculation process with flipper zero
```shell
usage: mfkey_extract.py [-h] [--cli] [--detect] [--extract LOGFILE]
                        [--clean-cache] [--clean-mfkey32-log] [--bkp-user-dict]
                        [--rm-dict-user]

Extracts Mifare values from flipper or a local mfkey32.log file, computes the
key's using mfkey32v2 and uploads them to flipper. The new computed key's will
added to the content of the "/SD/nfc/assets/mf_classic_dict_user.nfc" file. The
cli and detect mode are Linux only.

options:
  -h, --help           show this help message and exit
  --cli                Extract the values via flipper CLI, compute the key's
                       and upload them to flipper (full auto mode)
  --detect             Detect Flipper Zero Device - prints only the block
                       device
  --extract LOGFILE    Extract Keys from a local mfkey32.log file and creates a
                       "mf_classic_dict_user.nfc" file.
  --clean-cache        Removes all files in the (/SD/nfc/.cache) directory.
  --clean-mfkey32-log  Cleans the mfkey32.log file from flipper.
  --bkp-user-dict      Creates a backup of the "mf_classic_dict_user.nfc" file.
                       The backup file will be placed in the same dir on the
                       flipper.
  --rm-dict-user       Removes the "mf_classic_dict_user.nfc" file from the
                       flipper.

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

**Extra features**
- clean-cache: remove all cache files from flipper `/SD/nfc/.cache/` to prevent reading errors
- clean-mfkey32-log: removes the `/SD/nfc/.mfkey32.log` file from flipper to create clean captures using `Detect Reader`
- bkp-user-dict: Creates a backup of the `mf_classic_dict_user.nfc` file named `mf_classic_dict_user.nfc.bkp` (/SD/nfc/assets/mf_classic_dict_user.nfc.bkp)
- rm-dict-user: Removes the `/SD/nfc/assets/mf_classic_dict_user.nfc` file from flipper

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

## After Key Calculation 
Once your keys have been outut by Mfkey you can now take the keys collected and add them to your `mf_classic_dict.nfc` and `mf_classic_dict_user.nfc` files. be sure to add them to the top of your dictionary. 

Once added, clear the cache of your flipper and re scan your initial card. You should now notice more keys are found in the process of scanning the card 


