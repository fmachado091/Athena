# comparar saida produzida com saida esperada

# receber 3 argumentos (in, out, code)
# in e out vem do banco de dados
# code vem do upload do aluno
# code pode ser .c, .cpp, .zip ou .rar

# rodar codigo e gerar saida
# comparar saida produzida com saida esperada
# inicialmente apenas faz o diff pra ver se sao identicas
# e retorna a saida do diff se forem diferentes
# se forem iguais retorna "saidas iguais"

# vou supor que o arquivo com a saida eh o arquivo /compiler/saida_esperada.txt

# enviar resultados para a pagina criada

import subprocess
import os


def mover(entrada, saida, codigo):
    ans = ""

    directory = os.path.dirname(os.path.realpath(__file__))
    os.chdir(directory)

    os.chdir("compiler")

    with open('entrada.txt', 'wb+') as destination:
        for chunk in entrada.chunks():
            destination.write(chunk)

    with open('saida.txt', 'wb+') as destination:
        for chunk in saida.chunks():
            destination.write(chunk)

    with open('codigo.cpp', 'wb+') as destination:
        for chunk in codigo.chunks():
            destination.write(chunk)

    command = "mv codigo.cpp code/"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    process.wait()
    out, err = process.communicate()
    ans += out + '\n'

    command = "mv entrada.txt ../runner"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    process.wait()
    out, err = process.communicate()
    ans += out + '\n'

    command = "mv saida.txt ../runner"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    process.wait()
    out, err = process.communicate()
    ans += out + '\n'

    # executar compile.py
    command = "python compile.py"
    process = subprocess.Popen(command, stdout=subprocess.PIPE,
     stderr=subprocess.PIPE, shell=True)
    process.wait()
    out, err = process.communicate()
    ans += err + '\n'
    if err != '':
        return ans

    # mover programa.out de /compiler para /runner
    command = "mv programa.out ../runner"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    process.wait()
    out, err = process.communicate()
    ans += out + '\n'

    # muda diretorio para pasta runner
    os.chdir("../runner")

    # executar runner.py
    command = "python runner.py"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    process.wait()
    out, err = process.communicate()
    ans += out + '\n'

    # diff das saidas
    command = "diff saida.txt ../compiler/saida_esperada.txt"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    process.wait()
    outdiff, err = process.communicate()
    ans += outdiff + '\n'

    os.chdir(directory)
    os.chdir("compiler/code")

    command = "rm * -fv"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    process.wait()
    out, err = process.communicate()
    ans += out + '\n'

    os.chdir(directory)

    ans += '\n'

    if outdiff != "":
        return ans
    else:
        return "saidas iguais"
