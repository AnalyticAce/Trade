import sys

class Debugger:
    def print(self, message):
        print(message, file=sys.stderr)
