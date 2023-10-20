from termcolor import colored

class Text:
    ok      = colored("[OK]", 'green', attrs=['bold'])
    failed  = colored("[FAILED]", 'red', attrs=['bold'])
    

if __name__ == "__main__":
	print(
		Text.ok,
		Text.failed
	)