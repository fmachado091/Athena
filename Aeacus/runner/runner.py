import subprocess
import resource


def _set_limits():
    megabyte = 1000*1000
    resource.setrlimit(resource.RLIMIT_CORE, (10*megabyte, 10*megabyte))
    resource.setrlimit(resource.RLIMIT_CPU, (1, 1))
    resource.setrlimit(resource.RLIMIT_FSIZE, (1*megabyte, 1*megabyte))
    resource.setrlimit(resource.RLIMIT_DATA, (100*megabyte, 100*megabyte))
    resource.setrlimit(resource.RLIMIT_STACK, (100*megabyte, 100*megabyte))
    resource.setrlimit(resource.RLIMIT_RSS, (100*megabyte, 100*megabyte))
    resource.setrlimit(resource.RLIMIT_NPROC, (0, 0))
    resource.setrlimit(resource.RLIMIT_MEMLOCK, (0, 0))
    resource.setrlimit(resource.RLIMIT_AS, (100*megabyte, 100*megabyte))


saida = open("saida.txt", "w")
erro = open("erro.txt", "w")
entrada = open("entrada.txt", "r")
process = subprocess.Popen(
    "./programa.out",
    preexec_fn=_set_limits,
    stdin=entrada,
    stderr=erro,
    stdout=saida,
)
process.wait()
out, err = process.communicate()
code = process.poll()
if (code == -9):
    print("Time Limit Exceeded")
elif (code == -6):
    print("Memory Exceeded")
elif (code == -11):
    print("Segmentation Fault")
elif (code == -8):
    print("Division by zero")
