import tempfile
import base64
import subprocess
import os


f = "executable.exe"

path = tempfile.mkstemp()


result = subprocess.call(path)
