from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('relatorios/obras/', views.relatorio_obras, name='relatorio_obras'),
    path('projeto/<int:pk>/editar/', views.projeto_arquiteto_editar, name='projeto_arquiteto_editar'),

    # Autenticação
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register_view, name='register'),
    
    # Calendários
    path('calendario/', views.calendario_view, name='calendario'),
    path('calendario/pessoal/', views.calendario_pessoal_view, name='calendario_pessoal'),
    
    # API
    path('api/projetos/', views.api_projetos, name='api_projetos'),
    path('api/projetos/create/', views.api_criar_projeto, name='api-criar-projeto'),
    
    # CRUD Clientes
    path('clientes/', views.ClienteListView.as_view(), name='cliente_list'),
    path('clientes/novo/', views.ClienteCreateView.as_view(), name='cliente_create'),
    path('clientes/<int:pk>/editar/', views.ClienteUpdateView.as_view(), name='cliente_update'),
    path('clientes/<int:pk>/excluir/', views.ClienteDeleteView.as_view(), name='cliente_delete'),
    
    # CRUD StatusProjeto
    path('status/', views.StatusProjetoListView.as_view(), name='statusprojeto_list'),
    path('status/novo/', views.StatusProjetoCreateView.as_view(), name='statusprojeto_create'),
    path('status/<int:pk>/editar/', views.StatusProjetoUpdateView.as_view(), name='statusprojeto_update'),
    path('status/<int:pk>/excluir/', views.StatusProjetoDeleteView.as_view(), name='statusprojeto_delete'),
    
    # CRUD Projetos
    path('projetos/', views.ProjetoListView.as_view(), name='projeto_list'),
    path('projetos/novo/', views.ProjetoCreateView.as_view(), name='projeto_create'),
    path('projetos/<int:pk>/editar/', views.ProjetoUpdateView.as_view(), name='projeto_update'),
    path('projetos/<int:pk>/excluir/', views.ProjetoDeleteView.as_view(), name='projeto_delete'),
    
    # Edição para arquitetos
    path('projeto/<int:pk>/editar-arquiteto/', views.projeto_arquiteto_update, name='projeto_arquiteto_update'),
    
    # Página inicial redireciona para o calendário apropriado
    path('', views.home_redirect, name='home'),
]