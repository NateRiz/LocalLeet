from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys


class Problem:
    def __init__(self, pid, title, acceptance, difficulty):
        self.problem_id = pid
        self.title = title
        self.acceptance = acceptance
        self.difficulty = difficulty


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
    """.format("[L]ist","List problems in order.",
               "[D]ownload <number>","Downloads the problem description and template.",
               "[S]ubmit <number>","Attempts to upload the current file for submission. Must be logged in.")
    )


def submit_code():
    pass


def download_problem():
    pass

def list_problems():
    url = "https://leetcode.com/problemset/all/"
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(chrome_options=options)
    wait = WebDriverWait(driver,10)
    driver.get(url)

    problems = list()

    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'tr')))
        tablerows = driver.find_elements_by_tag_name("tr")
    except Exception as e:
        print("Timeout: Request to Leetcode has timed out and was unable to fetch problems.")
        print(e)
        return


    problems = list()

    for tr in tablerows:
        if "%" in tr.text:
            parsed = tr.text.split("\n")
            problems.append(Problem(parsed[0].strip(),#id
                                    parsed[1].strip(),#name
                                    parsed[2].split()[0].strip(),#acceptance
                                    parsed[2].split()[1].strip()))#difficulty

    for p in problems:
        print("{:<16}{:<64}{:<16}{:<16}".format(p.problem_id, p.title, p.acceptance, p.difficulty))










if __name__ == "__main__":
    args = [a.lower() for a in sys.argv[1::]]
    if len(args)==0 or args[0] in ["help","usage","commands"]:
        usage()
    elif args[0] in ["list","l"]:
        list_problems()
