from rest_framework import serializers
from .models import Projeto

class ProjetoSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    start = serializers.DateTimeField(source='data_agendada')
    status_desc = serializers.CharField(source='status.descricao')
    status_cor = serializers.CharField(source='status.cor') 
    cliente_nome = serializers.CharField(source='cliente.nome')
    usuario_nome = serializers.CharField(source='usuario.username')

    
    class Meta:
        model = Projeto
        fields = ['id', 'title', 'start', 'status_desc', 'status_cor', 'cliente_nome', 'usuario_nome', 'observacao']
    
    def get_title(self, obj):
        return f"{obj.descricao} - {obj.cliente.nome}"