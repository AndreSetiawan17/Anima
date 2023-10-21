from termcolor import colored as col

class Text:
    ok      = f"[{col('OK', 'green', attrs=['bold'])}]"
    failed  = f"[{col('Failed', 'red', attrs=['bold'])}]"


class Msg:
	"""
		Error Messege
	"""

	PermissionError = f"{col('Access denied','red',attrs=['bold'])}, you can run this code with {col('sudo',attrs=['bold'])}"
	FileFolderNotFound = f"{col('File/Folder not found','red' , attrs=['bold'])}"

if __name__ == "__main__":
	print(
		Msg.PermissionError,
		Msg.FileFolderNotFound,

		Text.ok,
		Text.failed,
	)