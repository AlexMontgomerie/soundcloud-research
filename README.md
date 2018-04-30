# Description

This is a tool to gather information on users on soundcloud and help obtain primary research on musicians within london.

# Script dependencies
To install all dependencies, firstly you must have python 3.5 running. You will also need to download python libraries, which can be done by:
```
sudo pip3 install requirements.txt
```

# Example Script
The `soundcloud-research.py` script contains a class which holds all the functions to execute collecting the relevant information. Usage is shown below:

```
python3 soundcloud-research-users.py -s <search url> -o <output file location>
```
an example search url would be `https://soundcloud.com/search/people?q=london` and output file such as `./data/users.json`.

# TODO
 - add messaging automation
 - collect track information
