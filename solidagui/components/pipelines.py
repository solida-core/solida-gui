from django.conf import settings
from components.configs import SolidaConfigFile

import os


class Pipelines(object):
    def __init__(self):
        conf = SolidaConfigFile(yaml_file=settings.SOLIDA_CONFIG_FILE)
        self.pipelines = conf.get_pipelines_section()

    def get_pipelines_list(self):
        pipe_list = list()
        for k, v in self.pipelines.items():
            split_url = v.get('url').split('/')
            short_url = os.path.join(split_url[-2], split_url[-1].split('.')[0])
            v.update(dict(short_url=short_url))
            pipe_list.append(v)

        return pipe_list

    def get_pipelines_tuples(self, n=2):
        pipelines = self.get_pipelines_list()
        it = [iter(pipelines)] * n
        tuples = list(zip(*it))
        mod = len(pipelines) % n
        if mod != 0:
            tuples.append(pipelines[-mod:])
        return tuples

