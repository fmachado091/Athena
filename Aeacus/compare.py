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
from pprint import pprint

DIRETORIO_DO_ARQUIVO = os.path.dirname(os.path.realpath(__file__))


def _is_blank(myString):
    return not(myString and myString.strip())


def _copy_file(origem, destino):
    with open(destino, 'wb+') as destination:
        destination.write(origem)


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

    out, err = _deletar_codigo_antigo()
    if not _is_blank(err):
        return ("CE", "error ao deletar arquivos antigos:\n" + out)

    # prepara arquivo de codigo e compila
    os.chdir(DIRETORIO_DO_ARQUIVO)
    os.chdir("compiler/code")
    _bytes_to_text(codigo, 'codigo.cpp')

    out, err = compile.compile_cpp(
        os.path.join(DIRETORIO_DO_ARQUIVO, "compiler/code")
    )

    if not _is_blank(err):
        return ("CE", ("Error de compilacao!\n" + err).replace("\n", "<br>"))

    # mover programa.out de /compiler para /runner
    os.chdir(DIRETORIO_DO_ARQUIVO)
    _execute("mv compiler/code/programa.out runner")

    # prepara arquivos de entrada/saida e roda
    os.chdir(DIRETORIO_DO_ARQUIVO)
    os.chdir("runner")
    _copy_file(entrada, 'entrada.txt')
    _copy_file(resposta, 'resposta.txt')

    out, err = _execute("python runner.py")
    if not _is_blank(err):
        return ("RTE", "erro de execucao\n" + out)

    # diff das saidas
    outdiff, err = _execute("cat saida.txt")
    num_diffs, err = _execute('diff -b saida.txt resposta.txt | grep -c "^>"')
    num_diffs.replace("\n", "")
    num_diffs = int(num_diffs)
    pprint(num_diffs)

    if num_diffs != 0:
        pprint(num_diffs)
        cabecalho = str(num_diffs) + "\n"
        return ("WA", cabecalho + outdiff)
    else:
        return ("AC", "saidas iguais")
