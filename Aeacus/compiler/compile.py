import subprocess
import os
from pyunpack import Archive

def unzip(file):
    command = 'unzip ' + file + ' -d ' + os.path.dirname(file)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    process.wait()

def unrar(file):
    command = 'unrar e ' + file  + ' ' + os.path.dirname(file)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    process.wait()

def descompactar():
    path = os.path.realpath('code')
    process = subprocess.Popen(
        'find ' + path + ' -name "*.rar" -o -name "*.zip"',
        stdout=subprocess.PIPE, shell=True
    )

    out, err = process.communicate()
    process.wait()
    files = out.split('\n')
    for file in files:
        filename, fileExt = os.path.splitext(file)
        if fileExt == '.zip':
            unzip(file)
        elif fileExt == '.rar':
            unrar(file)

def find_sources():
    path = os.path.realpath('code')
    process = subprocess.Popen(
        'find ' + path + ' -name "*.h" -o -name "*.cpp" -o -name "*.c" -o -name "*.a" ',
        stdout=subprocess.PIPE, shell=True
    )
    process.wait()
    out, err = process.communicate()
    return out

def move_file_to_code_root(file_path):
    path = os.path.abspath('code')
    file_name = os.path.basename(file_path)
    new_file_path = path + "/" + file_name
    if file_path != new_file_path:
        command = "mv " + file_path + " " + new_file_path
        print(command)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        process.wait()

descompactar()

files = find_sources().split('\n')
# remove strings vazias
files = filter(None, files)
for file in files:
    move_file_to_code_root(file)
files = find_sources().split('\n')
command = "g++ " 
for file in files:
    command += file + " "
command += " -g -pthread -pg -std=c++0x -o programa.out"

process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
process.wait()
out, err = process.communicate()
print(out)
print(err)
