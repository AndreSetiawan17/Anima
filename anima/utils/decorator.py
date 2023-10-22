from text import Messege as msg, Text



def coba(func):
    error = []
    
    def wrapper():
        try:
            func()
        except PermissionError:
            print(Text.failed)