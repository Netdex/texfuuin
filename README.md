# texfuuin
`This project is a work-in-progress.`

## Abstract
**texfuuin** plans to be a super lightweight textboard, akin to similar software like Kareha and 2ch.  
Currently in a prototyping phase.


## Running
```
git clone https://github.com/netdex/texfuuin.git
python3 -m virtualenv venv
pip3 install -r requirements.txt
vim config.py   # update configuration file now
python3 texfuuin.py
```

## Features
### Tripcodes
Similar to tripcodes in other textboards. Enter `username#tripcode` as the user parameter when making a new post. 
The tripcode will be salted, hashed, then truncated. If the tripcode matches `config.admin_trip`, it will receive 
special formatting.