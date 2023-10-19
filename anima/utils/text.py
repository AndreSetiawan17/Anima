from termcolor import colored

class Text:
    ok      = colored("OK", 'green', attrs=['bold'])
    failed  = colored("Failed", 'red', attrs=['bold'])