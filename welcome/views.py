from django.views.generic import TemplateView


class WelcomeView(TemplateView):
    Template_name = 'welcome/index.html'
