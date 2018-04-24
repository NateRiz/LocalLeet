import requests
import sys


def usage():
    print(
    """
LocalLeet 1.0.0
    
Usage: 
LocalLeet is a command line interface for retrieval and submission of problems from https://leetcode.com/.
    
Commands: leet <command>
  {:<32}{}
  {:<32}{}
  {:<32}{}
    """.format("list","List problems in order.","d <number>","Downloads the problem description and template.",
               "<number>","Attempts to upload the current file for submission. Must be logged in.")
    )


def submit_code():
    pass


def download_problem():
    print("!")












if __name__ == "__main__":
    args = [a.lower() for a in sys.argv[1::]]
    if len(args)==0 or args[1] in "help usage commands":
        usage()
    elif args[1] == "list":
        download_problem()
