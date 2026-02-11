# agenda/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Cliente, StatusProjeto, Projeto

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_arquiteto']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'is_arquiteto': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'telefone', 'email', 'endereco']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo do cliente'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(11) 99999-9999'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'cliente@email.com'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço completo'}),
        }

class StatusProjetoForm(forms.ModelForm):
    class Meta:
        model = StatusProjeto
        fields = ['descricao', 'cor']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descrição do status'}),
            'cor': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
        }

class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = ['cliente', 'descricao', 'status', 'usuario', 'data_agendada', 'observacao']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descrição do projeto'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'usuario': forms.Select(attrs={'class': 'form-select'}),
            'data_agendada': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Observações adicionais...'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usuario'].queryset = User.objects.filter(is_arquiteto=True)

class ProjetoArquitetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = ['status', 'data_agendada', 'observacao']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'data_agendada': forms.DateTimeInput(attrs={
                'class': 'form-control', 
                'type': 'datetime-local'
            }),
            'observacao': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'Observações sobre o projeto...'
            }),
        }