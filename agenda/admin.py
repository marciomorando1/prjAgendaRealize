from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Cliente, StatusProjeto, Projeto

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'is_arquiteto', 'is_staff', 'is_active']
    list_filter = ['is_arquiteto', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('is_arquiteto',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Adicionais', {'fields': ('is_arquiteto',)}),
    )

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'telefone', 'email']
    search_fields = ['nome', 'email']

@admin.register(StatusProjeto)
class StatusProjetoAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'cor', 'amostra_cor']
    
    def amostra_cor(self, obj):
        return format_html(
            '<span style="display: inline-block; width: 20px; height: 20px; background-color: {}; border: 1px solid #000;"></span>',
            obj.cor
        )
    amostra_cor.short_description = 'Cor'

@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'cliente', 'status', 'usuario', 'data_agendada']
    list_filter = ['status', 'usuario']
    search_fields = ['descricao', 'cliente__nome']