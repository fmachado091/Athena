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

# enviar resultados para a pagina criada

import subprocess
import os


def bytesTOtext(bytes, text):
    with open(text, 'wb+') as destination:
        for chunk in bytes.chunks():
            destination.write(chunk)


def execute(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    process.wait()
    return process.communicate()


def mover(entrada, saida, codigo):
    ans = ""

    directory = os.path.dirname(os.path.realpath(__file__))
    os.chdir(directory)

    os.chdir("compiler")

    bytesTOtext(entrada, 'entrada.txt')
    bytesTOtext(saida, 'resposta.txt')
    bytesTOtext(codigo, 'codigo.cpp')

    out, err = execute("mv codigo.cpp code/")
    ans += out + '\n'

    out, err = execute("mv entrada.txt ../runner")
    ans += out + '\n'

    out, err = execute("mv resposta.txt ../runner")
    ans += out + '\n'

    # executar compile.py
    command = "python compile.py"
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )
    process.wait()
    out, err = process.communicate()
    ans += err + '\n'
    if err != '':
        return ans

    # mover programa.out de /compiler para /runner
    out, err = execute("mv programa.out ../runner")
    ans += out + '\n'

    # muda diretorio para pasta runner
    os.chdir("../runner")

    # executar runner.py
    out, err = execute("python runner.py")
    ans += out + '\n'

    # diff das saidas
    outdiff, err = execute("diff saida.txt resposta.txt")
    ans += outdiff + '\n'

    os.chdir(directory)
    os.chdir("compiler/code")

    out, err = execute("rm * -fv")
    ans += out + '\n'

    os.chdir(directory)

    ans += '\n'

    if outdiff != "":
        return ans
    else:
        return "saidas iguais"
