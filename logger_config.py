import sys
import os
from datetime import datetime

class Logger(object):
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "a", encoding="utf-8")

    def write(self, message):
        if message.strip():
            timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
            self.terminal.write(f"{timestamp}{message}\n")
            self.log.write(f"{timestamp}{message}\n")
        elif message == "\n":
            self.terminal.write(message) # Mantiene la formattazione a video

    def flush(self):
        self.terminal.flush()
        self.log.flush()
