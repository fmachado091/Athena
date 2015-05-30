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
from Aeacus.compiler import compile

DIRETORIO_DO_ARQUIVO = os.path.dirname(os.path.realpath(__file__))

def _is_blank(myString):
    return not(myString and myString.strip())


def _bytes_to_text(bytes, text):
    with open(text, 'wb+') as destination:
        for chunk in bytes.chunks():
            destination.write(chunk)


def _execute(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    process.wait()
    return process.communicate()


# remove arquivos de codigo de outras compilacoes
def _deletar_codigo_antigo():
    os.chdir(DIRETORIO_DO_ARQUIVO)
    os.chdir("compiler/code")

    return _execute("rm * -fv")


def mover(entrada, resposta, codigo):

    out,err = _deletar_codigo_antigo()
    if not _is_blank(err):
        return "error ao deletar arquivos antigos:\n" + out

    # prepara arquivo de codigo e compila
    os.chdir(DIRETORIO_DO_ARQUIVO)
    os.chdir("compiler/code")
    _bytes_to_text(codigo, 'codigo.cpp')

    out, err = compile.compile_cpp(
        os.path.join(DIRETORIO_DO_ARQUIVO, "compiler/code")
    )

    if not _is_blank(err):
        return ("Error de compilacao!\n" + err).replace("\n", "<br>")

    # mover programa.out de /compiler para /runner
    os.chdir(DIRETORIO_DO_ARQUIVO)
    _execute("mv compiler/programa.out runner")

    # prepara arquivos de entrada/saida e roda
    os.chdir(DIRETORIO_DO_ARQUIVO)
    os.chdir("runner")
    _bytes_to_text(entrada, 'entrada.txt')
    _bytes_to_text(resposta, 'resposta.txt')

    out, err = _execute("python runner.py")
    if not _is_blank(err):
        return "erro de execucao\n" + out

    # diff das saidas
    outdiff, err = _execute("diff saida.txt resposta.txt")

    if not _is_blank(outdiff):
        outdiff = outdiff.replace("\n", "<br>")
        return outdiff
    else:
        return "saidas iguais"
