class Logger:
    def __init__(self):
        pass

    def log_exception(self, e: Exception) -> None:
        s = "Raised Exception"
        s += "\n"
        s += str(e)
        print(s)