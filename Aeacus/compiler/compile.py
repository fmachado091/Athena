import subprocess
import os


def _unzip(file):
    command = 'unzip ' + file + ' -d ' + os.path.dirname(file)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    process.wait()


def _unrar(file):
    command = 'unrar e ' + file + ' ' + os.path.dirname(file)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    process.wait()


def _descompactar(path_to_folder):
    process = subprocess.Popen(
        'find ' + path_to_folder + ' -name "*.rar" -o -name "*.zip"',
        stdout=subprocess.PIPE, shell=True
    )

    out, err = process.communicate()
    process.wait()
    files = out.split('\n')
    for file in files:
        filename, fileExt = os.path.splitext(file)
        if fileExt == '.zip':
            _unzip(file)
        elif fileExt == '.rar':
            _unrar(file)


def _find_sources(folder_path):
    process = subprocess.Popen(
        'find ' +
        folder_path +
        ' -name "*.h" -o -name "*.cpp" -o -name "*.c" -o -name "*.a" ',
        stdout=subprocess.PIPE, shell=True
    )
    process.wait()
    out, err = process.communicate()
    return out


def _move_file_to_code_root(folder_path, file_path):
    path = folder_path
    file_name = os.path.basename(file_path)
    new_file_path = path + "/" + file_name
    if file_path != new_file_path:
        command = "mv " + file_path + " " + new_file_path
        print(command)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        process.wait()


def compile_cpp(abs_path_to_folder):
    _descompactar(abs_path_to_folder)
    os.chdir(abs_path_to_folder)
    files = _find_sources(abs_path_to_folder).split('\n')
    # remove strings vazias
    files = filter(None, files)
    for file_path in files:
        _move_file_to_code_root(abs_path_to_folder, file_path)
    files = _find_sources(abs_path_to_folder).split('\n')
    command = "g++ "
    for file in files:
        command += os.path.basename(file) + " "
    command += " -g -pthread -pg -std=c++0x -o programa.out"

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    process.wait()
    out, err = process.communicate()
    return out, err
