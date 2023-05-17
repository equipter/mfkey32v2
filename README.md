

# Mfkey32 Version 2
Mfkey32v2 is a tool used to calculate Mifare Classic Keys from encrypted nonces obtained from the reader. 

**Note: Nonce in computer terminology means "Number used once"**


## Acknowledgements

 - [Mfkey Base Code](https://github.com/rfidresearchgroup/proxmark3)
 - [RRG Author's file](https://github.com/equipter/mfkey32v2/blob/main/AUTHORS.md)
 - [Bettse for assisting in development](https://gitlab.com/bettse)

| [Github](https://github.com/equipter) | [Twitter](https://twitter.com/Equip0x80) | [Reddit](https://www.reddit.com/user/equipter) |  [Discord](https://discord.gg/e9XzfG5nV5) |
| :---: | :---: | :---: | :---: | 

## Disclaimer

**No one involved in this project is responsible for how you use it. Always follow local laws and EULAs.**

## What is Mfkey32v2
Mfkey32v2 calculates Mifare Classic Sector keys from encrypted nonces collected by emulating the initial card and recording the interaction between the emulated card and the respective reader. 

While performing authentication, the reader will send "nonces" to the card which can be decrypted into keys. 

**Mfkey32v2 is not magic it cannot create you a working credential without an initial card. The Keys generated are not keys to open the door, they are keys to unlock and read sectors from inside the card itself.**

## Collecting Nonces with the FlipperZero 
1. After scanning your mifare classic and verifying you do not have all sector keys, save the file. 
2. Navigate to NFC -> Saved -> [Your File] -> detect reader 
3. Approach reader with flipperzero and observe nonces being collected. 
4. Once collected you can move on to cracking, see below the different methods (NOTE: They all do the same thing just in different ways) 
![image](https://user-images.githubusercontent.com/72751518/214213828-1fd5bef9-7978-4508-ac05-06a691de3a01.png)


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
* [Mifare Identification Procedure - AN10833](https://www.nxp.com/docs/en/application-note/AN10833.pdf)

# Support 
For support in using Mfkey32v2 message Equip#1515 on discord, submit a github issue or join my [discord](https://discord.gg/e9XzfG5nV5).
