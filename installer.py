import PyInstaller.__main__
import os
from config import OUTPUT_DIRECTORY, INPUT_DIRECTORY
from helpers import get_os_type, OSType


def make_adddata_filename(filename):
    return os.path.join(INPUT_DIRECTORY, filename)


def prepare_encrypted_executable(filename):
    



def run():
    PyInstaller.__main__.run([
        '-F',
        '--onefile',
        '--windowed',
        '--add-data',
        make_adddata_filename('setup.exe') + ':.',
        '--distpath',
        OUTPUT_DIRECTORY,
        'executable.py',
        # TODO: Add encryption :)
    ])


run()
