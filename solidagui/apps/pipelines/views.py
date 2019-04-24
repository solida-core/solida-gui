from django.views.generic.base import TemplateView
from components.pipelines import Pipelines


class BrowseView(TemplateView):
    template_name = 'pipelines/browse.html'

    def get_context_data(self, **kwargs):
        context = super(BrowseView, self).get_context_data(**kwargs)
        pipelines = Pipelines()
        context['pipelines'] = pipelines.get_pipelines_tuples(n=2)
        return context