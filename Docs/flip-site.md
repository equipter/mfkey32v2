
## Using Flipper Web Tool

### Using Detect Reader using a saved card
In the latest release, you can use detect reader using a saved card. This method is the recommended one because it won't use a fixed UID like normal detect reader uses and also it is more discreet than using a computer connected to your Flipper.
 
 
![](https://user-images.githubusercontent.com/45500329/201108244-7dc02b7a-fd82-4446-85e3-c44e852c69b7.gif)

approach the reader while doing the detect reader function on your saved file. Once nonce collection is completed an outputted mfkey.log file should appear in your NFC directory. 

## Using Flipper website
if you are unable to or don't know how to compile mfkey32v2, you can also use [Flipper's web tool version of mfkey32v2](https://lab.flipper.net/nfc-tools)
 
1. connect your flipper, make sure qFlipper or any other serial connection to the device is closed. 
2. go to the link above
3. press `GIVE ME THE KEYS` button
4. it will pull your log file, calculate the keys and add them to your dictionary.
 
**KEEP IN MIND**: this method will automatically replace your `mf_classic_user_dict.nfc` dictionary with a file containing just these new keys, so make sure you have a backup as this method will remove any keys you currently have stored in `mf_classic_user_dict.nfc`

---
Once added, clear the cache of your flipper and re scan your initial card. you should now notice more keys are found in the process of scanning the card