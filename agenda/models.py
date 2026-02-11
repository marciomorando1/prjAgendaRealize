# agenda/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    is_arquiteto = models.BooleanField(default=False)
    
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='agenda_user_set',  # Nome personalizado
        related_query_name='agenda_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='agenda_user_set',  # Nome personalizado
        related_query_name='agenda_user',
    )
    
    def __str__(self):
        return f"{self.username} ({'Arquiteto' if self.is_arquiteto else 'Empresa'})"

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    email = models.EmailField()
    endereco = models.CharField(max_length=200)
    
    def __str__(self):
        return self.nome

class StatusProjeto(models.Model):
    descricao = models.CharField(max_length=50)
    cor = models.CharField(max_length=7, default='#3788d8')
    
    def __str__(self):
        return self.descricao

class Projeto(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=200)
    status = models.ForeignKey(StatusProjeto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    data_agendada = models.DateTimeField()
    observacao = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.descricao} - {self.cliente.nome}"