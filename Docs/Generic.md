
## Generic Usage

This document is for generic non-flipper usage of the mfkey32v2 tool.

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

## Standalone Usage

The command syntax for mfkey32v2 is:

`./mfkey32v2 <uid> <nt> <nr_0> <ar_0> <nt1> <nr_1> <ar_1>`

## Example Mfkey32v2 Usage
input:

` ./mfkey32v2 2a234f80 240bd022 ad2e1687 57e6f7e4 18a4bd3e accc1a23 6f10e401`

output:
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


## After Key Calculation 
Once your keys have been outut by Mfkey you can now use that key and attempt authentication on the sector described by your collection method
