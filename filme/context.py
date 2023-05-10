from .models import Filme


def lista_filmes_recente(request):
    lista_filmes = Filme.objects.all().order_by('-data')[0:6]
    if lista_filmes:
        filme_destaque = lista_filmes[0]
        
    else:
        filme_destaque = None
    return {"lista_filmes_recente":lista_filmes, "filme_destaque":filme_destaque}


def lista_filmes_emalta(request):
    lista_filmes = Filme.objects.all().order_by('-visualizacoes')[0:6]
    return {"lista_filmes_emalta":lista_filmes}