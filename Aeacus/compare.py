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

# from compiler import compile
import subprocess
import os


def isBlank(myString):
    return not(myString and myString.strip())


def concat(s1, s2):
    if not isBlank(s2):
        s1 += s2 + '\n'
    return s1


def bytesTOtext(bytes, text):
    with open(text, 'wb+') as destination:
        for chunk in bytes.chunks():
            destination.write(chunk)


def execute(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    process.wait()
    return process.communicate()


def mover(entrada, saida, codigo):
    ans = ''

    directory = os.path.dirname(os.path.realpath(__file__))
    os.chdir(directory)

    os.chdir("compiler")

    bytesTOtext(entrada, 'entrada.txt')
    bytesTOtext(saida, 'resposta.txt')
    bytesTOtext(codigo, 'codigo.cpp')

    out, err = execute("mv codigo.cpp code/")
    ans = concat(ans, out)

    out, err = execute("mv entrada.txt ../runner")
    ans = concat(ans, out)

    out, err = execute("mv resposta.txt ../runner")
    ans = concat(ans, out)

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
    ans = concat(ans, err)
    if not isBlank(err):
        return ans

    # mover programa.out de /compiler para /runner
    out, err = execute("mv programa.out ../runner")
    ans = concat(ans, out)

    # muda diretorio para pasta runner
    os.chdir("../runner")

    # executar runner.py
    out, err = execute("python runner.py")
    ans = concat(ans, out)

    # diff das saidas
    outdiff, err = execute("diff saida.txt resposta.txt")
    ans = concat(ans, outdiff)

    os.chdir(directory)
    os.chdir("compiler/code")

    out, err = execute("rm * -fv")
    ans = concat(ans, out)

    os.chdir(directory)

    ans += '\n'

    if not isBlank(outdiff):
        ans = ans.replace("\n", "<br />")
        return ans
    else:
        return "saidas iguais"
