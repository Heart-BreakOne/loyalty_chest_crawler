# Stream Raiders Loyalty chest crawler written in Python

## Use locally without having to set up discord or post to your own discord webhook:

It can also find offline captains doing good chests.<br>
The crawler needs the first first slot available.<br>
Because PVP and dungeons are shorter and they last as long as the dungeon is progressing or the captain stops playing the mode the time remaining is not displayed.
## There are two ways to add an account:
### 1. How to add an account:
Run ```python3 setup.py``` using the terminal or double click it to execute the file to install the required PyQt5 and PyQtWebEngine.<br>
Run ```python3 add_account.py``` using the terminal or double click it to execute the file. It will open a browser so you can login to your SR viewer account.
The account will be added and the browser will close.

### 2. How to add an account:
Rename ```.private_constants.py``` to ```private_constants.py``` by removing the leading dot and fill it with your credentials using the SR cookies.


## After the account has been added to run the crawler simply run ```python3 run.py``` using the terminal or double click it to execute the file.

## Filter the chests you want to see:
Open the file constants.py and edit ```"print"``` to ```True``` on the chests you would like to see and ```False``` on the chests you have no interest in seeing.

## Post to a discord webhook:
Open the file webhook.py and set ```discord``` to ```True``` and fill the ```webhook``` with your valid webhook URL.

Make sure to keep all of your credentials private.
