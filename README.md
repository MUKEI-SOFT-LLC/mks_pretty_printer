# Project
 Github code pretty printer like gist.
 If `pp.js` is requested the url of Github's branch or blob source code,
 it responds pretty prinable js code as `text/javascript` to browser.

 If the url contains hash based line region,
 `pp.js` only print the part of the full source file. 
For example,
(%23 is `#` character url encoded.)

* pp.js?url=https://github.com/path/to/blob/Sample.java%23L21-L34
   ** Only prints from 21 to 34 lines of Sample.java.
* pp.js?url=https://github.com/path/to/blob/Sample.java%23L21
   ** Only prints of 21 line.

It can print full source code if not specified hash based line region.
* pp.js?url=https://github.com/path/to/blob/Sample.java
 
# How to setup 

## prerequisite

Download Selenium Chrome driver and install it into valid $PATH place.
https://googlechromelabs.github.io/chrome-for-testing/

```bash
mkdir <your_directory> && cd <your_directory>
git clone https://github.com/MUKEI-SOFT-LLC/mks_pretty_printer
python3 -m venv venv
source ./venv/bin/activate
cd mks_pretty_printer
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
