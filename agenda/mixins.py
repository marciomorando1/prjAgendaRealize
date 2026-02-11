# agenda/mixins.py
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect

class EmpresaRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_arquiteto
    
    def handle_no_permission(self):
        return redirect('calendario_pessoal')

class ArquitetoRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_arquiteto
    
    def handle_no_permission(self):
        return redirect('calendario')