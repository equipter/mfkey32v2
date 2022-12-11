

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


# Support 
For support in using Mfkey32v2 message Equip#1515 on discord or submit a github issue
