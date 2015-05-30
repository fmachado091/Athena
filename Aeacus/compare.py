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


def _is_blank(myString):
    return not(myString and myString.strip())


def _concat(s1, s2):
    if not _is_blank(s2):
        s1 += s2 + '\n'
    return s1


def _bytes_to_text(bytes, text):
    with open(text, 'wb+') as destination:
        for chunk in bytes.chunks():
            destination.write(chunk)


def _execute(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    process.wait()
    return process.communicate()


def mover(entrada, saida, codigo):
    ans = ''

    directory = os.path.dirname(os.path.realpath(__file__))
    os.chdir(directory)

    os.chdir("compiler")

    _bytes_to_text(entrada, 'entrada.txt')
    _bytes_to_text(saida, 'resposta.txt')
    _bytes_to_text(codigo, 'codigo.cpp')

    out, err = _execute("mv codigo.cpp code/")
    ans = _concat(ans, out)

    out, err = _execute("mv entrada.txt ../runner")
    ans = _concat(ans, out)

    out, err = _execute("mv resposta.txt ../runner")
    ans = _concat(ans, out)

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
    ans = _concat(ans, err)
    if not _is_blank(err):
        return ans

    # mover programa.out de /compiler para /runner
    out, err = _execute("mv programa.out ../runner")
    ans = _concat(ans, out)

    # muda diretorio para pasta runner
    os.chdir("../runner")

    # executar runner.py
    out, err = _execute("python runner.py")
    ans = _concat(ans, out)

    # diff das saidas
    outdiff, err = _execute("diff saida.txt resposta.txt")
    ans = _concat(ans, outdiff)

    os.chdir(directory)
    os.chdir("compiler/code")

    out, err = _execute("rm * -fv")
    ans = _concat(ans, out)

    os.chdir(directory)

    ans += '\n'

    if not _is_blank(outdiff):
        ans = ans.replace("\n", "<br />")
        return ans
    else:
        return "saidas iguais"
