from Athena.models import Professor, Aluno


def checar_login_professor(request):

    if not request.user.is_authenticated():
        return False

    professor = Professor.objects.filter(user=request.user)

    return professor


def checar_login_aluno(request):

    if not request.user.is_authenticated():
        return False

    aluno = Aluno.objects.filter(user=request.user)

    return aluno
