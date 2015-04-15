import subprocess
import resource


def set_limits():
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
process = subprocess.Popen(
    "./programa.out",
    preexec_fn=set_limits,
    stderr=subprocess.PIPE,
    stdout=saida,
)
