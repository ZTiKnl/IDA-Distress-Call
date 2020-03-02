# IDA-Distress-Call
Send a Distress Call to Discord Channel when under attack

## Version  
Version 0.12  

## What it does:  
Whenever a user is interdicted, an event is created in the ED journal file.  
This plugin reads this event (Interdicted), gathers data, and pushes JSON formatted data to the [IDA-DC-Bot](https://github.com/ZTiKnl/IDA-DC-Bot).  
Data sent to the IDA-DC-Bot is processed and posted on a dedicated Discord channel.  

## How to use:  
1. Clone the repo to the EDMC plugin folder, or download and unzip to the EDMC plugin folder  
   (default: `c:\Users\%USERNAME%\AppData\Local\EDMarketConnector\plugins`)  
2. Request API key on webinterface  
3. Start up EDMC  
4. Insert API key into plugin by going to File -> Settings, tab IDA-Distress-Call, enter/paste the key, and hit OK  

There is an extra row in the main window of EDMC, labeled IDA DC.  
This row can have 5 different values:  
- `Idle`
  Not doing anything  

- `Sending Distress Call`  
  Sending data to the IDA-DC-Bot  
  
- `Distress Call sent`  
  The DC-Bot received data, process it, and sent it to Discord  

- `Fail: error code - short error message`  
  could be many things, the error code and short error message will be a hint/clue  
  The full error message can be found in EDMC log file, usually located in `%TMP%/EDMarketConnector.log`  

## Changes to make for use by another faction
Want to make this work for another faction, all you need to change here is 1 instance of the server url to push data to `http://distresscall.ztik.nl/api`  

## Disclaimer
This plugin is still under construction, ~~bugs~~ new features WILL appear unexpectedly.  
There is no license on this code, feel free to use it as you see fit.  
Patches are always welcome.  

## Thanks
- devnull & Plusran, wouldnt have gotten the plugin working so fast without your help  