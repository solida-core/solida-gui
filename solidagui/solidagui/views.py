from django.views.generic.base import TemplateView


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        return context


class DocsView(TemplateView):
    template_name = 'docs.html'

    def get_context_data(self, **kwargs):
        context = super(DocsView, self).get_context_data(**kwargs)
        return context


class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        return context