# LocalLeet
LocalLeet is a command line interface for retrieval and submission of problems from https://leetcode.com/.

##### Installation
```
 $ pip install Localleet
```
##### Setup
Automatically create an leet.ini file in ~/.config/localleet/leet.ini 
```
leet d 0
```
Fill in atleast the first two parameters:
```
ddir=C:/Leetcode
language=Python3
user=not_required
pass=not_required
```

##### Usage
Commands: leet <command>
  [L]ist                          List problems in order.
  [I]nfo                          Receives problem description and examples.
  [D]ownload <number>             Downloads the problem description and template.
  [S]ubmit <number>               Attempts to upload the current file for submission. Must be logged in.


