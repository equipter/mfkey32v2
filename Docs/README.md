
# Flipper Mobile App Usage
### Using Detect Reader using a saved card
In the latest release, you can use detect reader using a saved card. This method is the recommended one because it won't use a fixed UID like normal detect reader uses and also it is more discreet than using a computer connected to your Flipper.
 
 
![](https://user-images.githubusercontent.com/45500329/201108244-7dc02b7a-fd82-4446-85e3-c44e852c69b7.gif)

approach the reader while doing the detect reader function on your saved file. Once nonce collection is completed an outputted mfkey.log file should appear in your NFC directory. 
## Using the Flipper Mobile app
Once you have your saved .mfkey.log file, connect your flipper to the mobile companion app. 

navigate to "HUB" and you should see the Mfkey tool. Activate it and allow it to run. 

 
**KEEP IN MIND**: this method will automatically replace your `mf_classic_user_dict.nfc` dictionary with a file containing just these new keys, so make sure you have a backup as this method will remove any keys you currently have stored in `mf_classic_user_dict.nfc`

---

Once added, clear the cache of your flipper and re scan your initial card. you should now notice more keys are found in the process of scanning the card