from django.views.generic.base import TemplateView
from components.pipelines import Pipelines, Pipeline
from django.conf import settings

from django.http import HttpResponse
from django.template import loader, RequestContext


class BrowseView(TemplateView):
    template_name = 'pipelines/browse.html'

    def get_pipelines_layout(self, pipelines, n=2):
        it = [iter(pipelines)] * n
        layout = list(zip(*it))
        mod = len(pipelines) % n
        if mod != 0:
            layout.append(pipelines[-mod:])
        return layout

    def get_context_data(self, **kwargs):
        context = super(BrowseView, self).get_context_data(**kwargs)
        context['pipelines'] = self.get_pipelines_layout(Pipelines().pipelines)
        return context


def setup(request, pipeline_id):
    template = loader.get_template('pipelines/setup.html')

    pipeline = Pipeline(pipeline_id=pipeline_id, with_profiles=True)
    to_do = request.POST.dict().get("to_do")

    if to_do and 'load' in to_do:
        profile_id = request.POST.dict().get("profile_selected")
    elif to_do and 'save' in to_do:
        profile_id = request.POST.dict().get("profile_name")
        pipeline.create_profile(profile_id, request.POST.dict())
    else:
        profile_id = None

    context = dict(pipeline=pipeline,
                   profile=pipeline.get_profile(profile_id=profile_id if profile_id else settings.SOLIDA_PROFILE_NAME),
                   profile_id=profile_id
                   )

    return HttpResponse(template.render(context, request))


