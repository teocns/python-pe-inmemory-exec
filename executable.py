import tempfile
import base64
import subprocess
import os


f = "setup.exe"
path = tempfile.mkstemp()
result = subprocess.call(path)
