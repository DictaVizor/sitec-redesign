from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin



class LoginView(TemplateView):
    template_name = 'school/login.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class PanelView(LoginRequiredMixin,TemplateView):
    template_name = 'school/panel.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class SettingsView(LoginRequiredMixin,TemplateView):
    template_name = 'school/settings.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
        
class ReinscriptionView(LoginRequiredMixin,TemplateView):
    template_name = 'school/reinscription.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)   
        
class CycleAdvanceView(LoginRequiredMixin,TemplateView):
    template_name = 'school/cycle_advance.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)   
        
class KardexView(LoginRequiredMixin,TemplateView):
    template_name = 'school/kardex.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)   
        
class LogView(LoginRequiredMixin,TemplateView):
    template_name = 'school/log.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)