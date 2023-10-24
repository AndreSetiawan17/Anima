from termcolor import colored as col

class Messege:

	ok      = f"[{col('OK'.center(8), 'green', attrs=['bold'])}]"
	failed  = f"[{col('Failed'.center(8), 'red', attrs=['bold'])}]"

	PermissionError = f"{col('Access denied','red',attrs=['bold'])}, you can run this code with {col('sudo',attrs=['bold'])}"
	FileFolderNotFound = f"{col('File/Folder not found','red' , attrs=['bold'])}"


if __name__ == "__main__":
	print(
		Messege.ok,
		"\n",
		Messege.failed,
		sep=""
	)