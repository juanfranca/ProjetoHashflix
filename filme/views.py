from django.shortcuts import render, redirect, reverse
from .models import Filme, Usuario
from .forms import CriarUsuario, FormHomePage
from django.views.generic import TemplateView , ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

# def home(request):
#     return render(request, 'homepage.html')

class Homepage(FormView):
    template_name = 'homepage.html'
    form_class = FormHomePage

    def get(self, request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect('filme:homefilmes')
            else:
                return super().get(request, *args, **kwargs)

    def get_success_url(self):
        email = self.request.POST.get("email")
        usuario = Usuario.objects.filter(email=email)
        if usuario:
            return reverse('filme:login')
        else:
            return reverse('filme:criarconta')
    # def homefilmes(request):
#     filme = Filme.objects.all()
#     return render(request, 'homefilmes.html', {'filmes':filme})

class HomeFilmes(LoginRequiredMixin, ListView):
    template_name = 'homefilmes.html'
    model=Filme
    #create a list which name is  * object_list * 

class DetailFilme(LoginRequiredMixin, DetailView):
    template_name = 'detalhefilmes.html'
    model=Filme
    #create a unique object

    def get(self, request, *args, **kwargs):
        filme = self.get_object()
        filme.visualizacoes +=1
        filme.save()
        usuario = request.user
        usuario.filmes_vistos.add(filme)    
        return super().get(request, *args, **kwargs) #redireciona o usuário para a url final 


    def get_context_data(self, **kwargs):
        context = super(DetailFilme, self).get_context_data(**kwargs)
        filmes_relacionados = Filme.objects.filter(categoria=self.get_object().categoria)
        context['filmes_relacionados'] = filmes_relacionados
        return context
    
class PesquisaFilme(ListView):
    template_name = 'pesquisafilme.html'
    model = Filme

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('query')
        if termo_pesquisa:
            object_list = self.model.objects.filter(titulo__icontains=  termo_pesquisa)
            return object_list
        else:
            return None
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset is None:
            return render(request, 'filmenaoencontrado.html')
        elif not queryset.exists():
            return render(request, 'filmenaoencontrado.html')
        else:
            return super().get(request, *args, **kwargs)
        

class EditarPerfil(LoginRequiredMixin, UpdateView):
    template_name = 'editarperfil.html'
    model = Usuario
    fields = ['first_name', 'last_name', 'email']


    def get_success_url(self):
        return reverse('filme:homefilmes')

class CriarConta(FormView):
    template_name = 'criarconta.html'
    form_class = CriarUsuario

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('filme:login')


