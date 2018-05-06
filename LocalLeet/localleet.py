from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


import sys
import os

SETTINGS = {"ddir": "", "language": "", "username": "", "password": ""}


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
      {:<32}{}
        """.format("[L]ist", "List problems in order.",
                   "[I]nfo", "Receives problem description and examples.",
                   "[D]ownload <number>", "Downloads the problem description and template.",
                   "[S]ubmit <number>", "Attempts to upload the current file for submission. Must be logged in.")
    )


def get_settings():
    global SETTINGS
    accepted_languages = ['c++', 'java', 'python', 'python3', 'c', 'c#', 'javascript', 'ruby', 'swift', 'go', 'scala',
                          'kotlin']

    file = "leet.ini"
    if not os.path.exists(os.path.abspath(file)):
        create_config()
        return 0
    else:
        with open(file, "r")as settings:
            for line in settings:
                line = line.strip()
                if line[0:5:] == "ddir=":
                    SETTINGS["ddir"] = line[5::].strip()
                elif line[0:9:] == "language=":
                    SETTINGS["language"] = line[9::].strip().lower()
                elif line[0:5:] == "user=":
                    SETTINGS["username"] = line[5::].strip()
                elif line[0:5:] == "pass=":
                    SETTINGS["password"] = line[5::].strip()
                else:
                    return 0

    if SETTINGS["ddir"] == "" or SETTINGS["language"] == "":
        print("Please specify the download directory and language in \"leet.ini\"")
        return 0
    if not os.path.exists(SETTINGS["ddir"]):
        print("The specified download directory was not found.:\n{}".format(SETTINGS["ddir"]))
        return 0
    if not (SETTINGS["language"]in accepted_languages):
        print("Please choose a language from the following:\n{}".format("\n".join(accepted_languages)))
        return 0

    return 1


def create_config():
    file = "leet.ini"
    with open(file, "w")as settings:
        settings.write("ddir=\nlanguage=\nuser=\npass=")

    return


def submit_code():
    if not login():
        return

def download_problem(problem_number):
    url = "https://leetcode.com/problemset/all/?search={}".format(problem_number)
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome()  # chrome_options=options)
    wait = WebDriverWait(driver, 10)
    driver.get(url)

    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'tr')))
        tablerows = driver.find_elements_by_tag_name("tr")
        if len(tablerows) > 1:
            problem_url = tablerows[1].find_element_by_css_selector('a').get_attribute('href')

        else:
            print("No results found.")
            return

    except Exception as e:
        print("No results found.")
        print(e)
        return

    try:
        driver.get(problem_url)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "question-description")))
        description = driver.find_elements_by_tag_name("p")


    except Exception as e:
        print("A result was found, but the url was invalid.")
        print(e)
        return

    global SETTINGS
    comment_start = '/*'
    comment_end = "*/"
    if "python" in SETTINGS["language"]:
        comment_start = '"""'
        comment_end = comment_start

    filtered_description = list()
    for d in description:
        if d.text.strip() and not "Subscribe" in d.text and not "Example" in d.text:
            filtered_description.append(d.text)

    filtered_description = "".join(filtered_description).split(".")

    [d.text.strip() for d in description if "Subscribe" not in d.text and "Example" not in d.text]

    selected_language = ""

    while selected_language != SETTINGS["language"]:
        print("again because {}  !=  {}".format(selected_language, SETTINGS["language"]))
        try:
            dropdown_element = driver.find_element_by_class_name("Select-value-label")
            dropdown_element.click()

            language_dropdown = driver.find_element_by_class_name("Select-input")

            language_dropdown.send_keys(Keys.ARROW_DOWN)
            language_dropdown.send_keys(Keys.RETURN)

            selected_language_element = driver.find_element_by_class_name("Select-value")
            selected_language = selected_language_element.text.strip().lower()


        except Exception as e:
            print(e)

    try:
        code_mirror = driver.find_element_by_class_name("ReactCodeMirror")
    except Exception as e:
        print("Could not download code template.")
        print(e)
        return

    language_extensions = {"java": "java", "c++": "cpp", "python": "py", "python3": "py", "c": "c", "c#": "cs",
                           "javascript": "js", "ruby": "rb", "swift": "swift", "go": "go", "scala": "scala",
                           "kotlin": "kt"}

    with open("Leetcode{}.{}".format(problem_number, language_extensions[SETTINGS["language"]]), "w") as file:
        file.write(comment_start + "\n")

        for d in filtered_description:
            file.write("{}\n".format(d))

        file.write("\n")

        file.write(comment_end + "\n\n")

        for t in code_mirror.text:
            if not t.strip().isdigit():  # Line Numbers
                file.write(t)


def list_problems():
    url = "https://leetcode.com/problemset/all/"
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(chrome_options=options)
    wait = WebDriverWait(driver, 10)
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
            problems.append(Problem(parsed[0].strip(),  # id
                                    parsed[1].strip(),  # name
                                    parsed[2].split()[0].strip(),  # acceptance
                                    parsed[2].split()[1].strip()))  # difficulty

    print("{:<16}{:<64}{:<16}{:<16}".format("#", "Title", "Acceptance", "Difficulty"))
    for p in problems:
        print("{:<16}{:<64}{:<16}{:<16}".format(p.problem_id, p.title, p.acceptance, p.difficulty))


def get_problem_info(problem_number):
    url = "https://leetcode.com/problemset/all/?search={}".format(problem_number)
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome()  # chrome_options=options)
    wait = WebDriverWait(driver, 10)
    driver.get(url)

    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'tr')))
        tablerows = driver.find_elements_by_tag_name("tr")
        if len(tablerows) > 1:
            problem_url = tablerows[1].find_element_by_css_selector('a').get_attribute('href')

        else:
            print("No results found.")
            return

    except Exception as e:
        print("No results found.")
        print(e)
        return

    example_elem = None
    try:
        driver.get(problem_url)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "question-description")))
        problem_elem = driver.find_element_by_class_name("question-description")
        description_elem = problem_elem.find_elements_by_tag_name("p")
        example_elem = problem_elem.find_elements_by_tag_name("pre")


    except Exception as e:
        print("A result was found, but the url was invalid.")
        print(e)
        return

    description = "".join([d.text.strip() for d in description_elem])


    print("____________________________________________________________________________")
    print("Problem {}:".format(problem_number))
    for d in description.split("."):
        if "example" not in d.lower() and "subscribe" not in d.lower():
            print("{}.\n".format(d.strip()))


    print("\n\n")
    if example_elem:
        for i,e in enumerate(example_elem):
            print("\n\nExample {}:\n{}".format(i, e.text))


    print("____________________________________________________________________________")


if __name__ == "__main__":
    args = [a.lower() for a in sys.argv[1::]]
    if len(args) == 0 or args[0] in ["help", "usage", "commands"]:
        usage()
    elif args[0] in ["list", "l"]:
        list_problems()
    elif args[0] in ["download", "d"]:
        if len(args) > 1 and args[1].isdigit():
            if get_settings():
                download_problem(args[1])
            else:
                print("Your user settings could not be read."
                      "If this is your first time using LocalLeet, "
                      'please make sure all of the required settings have been set in "leet.ini"')
        else:
            print("Please specify a problem number to download. eg: leet d 24")
    elif args[0] in ["submit", "s"]:
        if len(args) > 1:
            if get_settings():
                submit_code()
        else:
            print("Please specify the problem number or file name to submit. eg: leet s 24")
    elif args[0] in ["info","information","i"]:
        if len(args)>1 and args[1].isdigit():
                get_problem_info(args[1])
        else:
            print("Please specify a problem number for its description. eg: leet i 24")

