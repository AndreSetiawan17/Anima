import os

class Log:
    log_path = os.path.sep.join(__file__.split(os.path.sep)[:-1])




try:
    if os.path.exists("../log"):
        os.mkdir("../log")

except PermissionError:
    raise PermissionError("Run this code with sudo")