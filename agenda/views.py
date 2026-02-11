from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib import messages 
from django.db.models import Count, Q
from datetime import datetime
from rest_framework import status

from .models import Cliente, StatusProjeto, Projeto, User
from .forms import ClienteForm, StatusProjetoForm, ProjetoForm, ProjetoArquitetoForm, CustomUserCreationForm
from .mixins import EmpresaRequiredMixin, ArquitetoRequiredMixin
from .serializers import ProjetoSerializer

# Autenticação
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_arquiteto:
                return redirect('calendario_pessoal')  # redirecionar para calendário pessoal
            else:
                return redirect('calendario')  # Empresa vai para calendário geral
        else:
            # Mensagem de erro
            messages.error(request, 'Usuário ou senha inválidos')
    return render(request, 'agenda/login.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('calendario')
            # login(request, user)
            # if user.is_arquiteto:
            #     return redirect('calendario_pessoal')
            # else:
            #     return redirect('calendario')
    else:
        form = CustomUserCreationForm()
    return render(request, 'agenda/register.html', {'form': form})

# Views do Calendário
@login_required
def calendario_view(request):
    if request.user.is_arquiteto:
        return redirect('calendario_pessoal')
    
    arquitetos = User.objects.filter(is_arquiteto=True)
    selected_arquiteto = request.GET.get('usuario_id')
    
    context = {
        'arquitetos': arquitetos,
        'selected_arquiteto': selected_arquiteto,
    }
    return render(request, 'agenda/calendario.html', context)

@login_required
def calendario_pessoal_view(request):
    if not request.user.is_arquiteto:
        return redirect('calendario')
    return render(request, 'agenda/calendario_pessoal.html')

# API Views
@api_view(['GET'])
@login_required
def api_projetos(request):
    usuario_id = request.GET.get('usuario_id')
    
    if request.user.is_arquiteto:
        projetos = Projeto.objects.filter(usuario=request.user)
    elif usuario_id:
        projetos = Projeto.objects.filter(usuario_id=usuario_id)
    else:
        projetos = Projeto.objects.all()
    
    serializer = ProjetoSerializer(projetos, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@login_required
def api_criar_projeto(request):
    serializer = ProjetoSerializer(data=request.data)
    
    if serializer.is_valid():
        # Associa automaticamente o usuário logado
        projeto = serializer.save(usuario=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# CRUD Clientes
class ClienteListView(LoginRequiredMixin, EmpresaRequiredMixin, ListView):
    model = Cliente
    template_name = 'agenda/cliente_list.html'

class ClienteCreateView(LoginRequiredMixin, EmpresaRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'agenda/cliente_form.html'
    success_url = reverse_lazy('cliente_list')

class ClienteUpdateView(LoginRequiredMixin, EmpresaRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'agenda/cliente_form.html'
    success_url = reverse_lazy('cliente_list')

class ClienteDeleteView(LoginRequiredMixin, EmpresaRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'agenda/cliente_confirm_delete.html'
    success_url = reverse_lazy('cliente_list')

# CRUD StatusProjeto
class StatusProjetoListView(LoginRequiredMixin, EmpresaRequiredMixin, ListView):
    model = StatusProjeto
    template_name = 'agenda/statusprojeto_list.html'

class StatusProjetoCreateView(LoginRequiredMixin, EmpresaRequiredMixin, CreateView):
    model = StatusProjeto
    form_class = StatusProjetoForm
    template_name = 'agenda/statusprojeto_form.html'
    success_url = reverse_lazy('statusprojeto_list')

class StatusProjetoUpdateView(LoginRequiredMixin, EmpresaRequiredMixin, UpdateView):
    model = StatusProjeto
    form_class = StatusProjetoForm
    template_name = 'agenda/statusprojeto_form.html'
    success_url = reverse_lazy('statusprojeto_list')

class StatusProjetoDeleteView(LoginRequiredMixin, EmpresaRequiredMixin, DeleteView):
    model = StatusProjeto
    template_name = 'agenda/statusprojeto_confirm_delete.html'
    success_url = reverse_lazy('statusprojeto_list')

# CRUD Projetos
class ProjetoListView(LoginRequiredMixin, EmpresaRequiredMixin, ListView):
    model = Projeto
    template_name = 'agenda/projeto_list.html'

class ProjetoCreateView(LoginRequiredMixin, EmpresaRequiredMixin, CreateView):
    model = Projeto
    form_class = ProjetoForm
    template_name = 'agenda/projeto_form.html'
    success_url = reverse_lazy('projeto_list')

class ProjetoUpdateView(LoginRequiredMixin, EmpresaRequiredMixin, UpdateView):
    model = Projeto
    form_class = ProjetoForm
    template_name = 'agenda/projeto_form.html'
    success_url = reverse_lazy('projeto_list')

class ProjetoDeleteView(LoginRequiredMixin, EmpresaRequiredMixin, DeleteView):
    model = Projeto
    template_name = 'agenda/projeto_confirm_delete.html'
    success_url = reverse_lazy('projeto_list')

# Views para Arquitetos
@login_required
def projeto_arquiteto_update(request, pk):
    if not request.user.is_arquiteto:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': 'Acesso negado'})
        return redirect('calendario_pessoal')
    
    projeto = get_object_or_404(Projeto, pk=pk, usuario=request.user)
    
    if request.method == 'POST':
        form = ProjetoArquitetoForm(request.POST, instance=projeto)
        if form.is_valid():
            form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('calendario_pessoal')
        else:
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = error_list[0]
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': errors})
    
    # GET request - retornar o formulário
    form = ProjetoArquitetoForm(instance=projeto)
    return render(request, 'agenda/projeto_arquiteto_form.html', {'form': form, 'projeto': projeto})

# agenda/views.py - adicionar esta view
@login_required
def projeto_arquiteto_editar(request, pk):
    """View para edição de projeto em página completa (para arquitetos)"""
    if not request.user.is_arquiteto:
        return redirect('calendario_pessoal')
    
    projeto = get_object_or_404(Projeto, pk=pk, usuario=request.user)
    
    if request.method == 'POST':
        form = ProjetoArquitetoForm(request.POST, instance=projeto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Projeto atualizado com sucesso!')
            return redirect('calendario_pessoal')
    else:
        form = ProjetoArquitetoForm(instance=projeto)
    
    return render(request, 'agenda/projeto_arquiteto_editar.html', {
        'form': form, 
        'projeto': projeto
    })

class StatusProjetoListView(LoginRequiredMixin, EmpresaRequiredMixin, ListView):
    model = StatusProjeto
    template_name = 'agenda/statusprojeto_list.html'

class StatusProjetoCreateView(LoginRequiredMixin, EmpresaRequiredMixin, CreateView):
    model = StatusProjeto
    form_class = StatusProjetoForm
    template_name = 'agenda/statusprojeto_form.html'
    success_url = reverse_lazy('statusprojeto_list')

class StatusProjetoUpdateView(LoginRequiredMixin, EmpresaRequiredMixin, UpdateView):
    model = StatusProjeto
    form_class = StatusProjetoForm
    template_name = 'agenda/statusprojeto_form.html'
    success_url = reverse_lazy('statusprojeto_list')

class StatusProjetoDeleteView(LoginRequiredMixin, EmpresaRequiredMixin, DeleteView):
    model = StatusProjeto
    template_name = 'agenda/statusprojeto_confirm_delete.html'
    success_url = reverse_lazy('statusprojeto_list')

def home_redirect(request):
    """Redireciona para a página inicial apropriada baseada no tipo de usuário"""
    if request.user.is_authenticated:
        if request.user.is_arquiteto:
            return redirect('calendario_pessoal')
        else:
            return redirect('calendario')
    else:
        return redirect('login')
    
@login_required
def relatorio_obras(request):
    """View para gerar relatório de obras com filtros"""
    # Obter todos os status e arquitetos para os filtros
    status_list = StatusProjeto.objects.all()
    arquitetos = User.objects.filter(is_arquiteto=True)
    
    # Inicializar filtros
    status_filter = request.GET.get('status')
    arquiteto_filter = request.GET.get('arquiteto')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    
    # Query base
    if request.user.is_arquiteto:
        # Arquitetos só veem suas próprias obras
        obras = Projeto.objects.filter(usuario=request.user)
    else:
        # Empresa vê todas as obras
        obras = Projeto.objects.all()
    
    # Aplicar filtros
    if status_filter:
        obras = obras.filter(status_id=status_filter)
    
    if arquiteto_filter:
        obras = obras.filter(usuario_id=arquiteto_filter)
    
    if data_inicio:
        try:
            data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d')
            obras = obras.filter(data_agendada__date__gte=data_inicio_obj)
        except ValueError:
            pass
    
    if data_fim:
        try:
            data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d')
            obras = obras.filter(data_agendada__date__lte=data_fim_obj)
        except ValueError:
            pass
    
    # Ordenar por data
    obras = obras.order_by('data_agendada')
    
    # Estatísticas totais
    total_obras = obras.count()
    obras_por_status = obras.values('status__descricao', 'status__cor').annotate(total=Count('id'))
    obras_por_arquiteto = obras.values('usuario__username', 'usuario__first_name', 'usuario__last_name').annotate(total=Count('id'))
    
    context = {
        'obras': obras,
        'status_list': status_list,
        'arquitetos': arquitetos,
        'status_filter': status_filter,
        'arquiteto_filter': arquiteto_filter,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'total_obras': total_obras,
        'obras_por_status': obras_por_status,
        'obras_por_arquiteto': obras_por_arquiteto,
    }
    
    return render(request, 'agenda/relatorio_obras.html', context)