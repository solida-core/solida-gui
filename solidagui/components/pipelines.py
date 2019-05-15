from django.conf import settings
from components.configs import SolidaConfigFile
from components.profiles import Profiles, Profile
from components.solida import Solida

import os


class Pipeline(object):
    def __init__(self, pipeline_id, pipeline_dict=None, with_profiles=False):
        pipeline_dict = pipeline_dict if pipeline_dict else self.__get_pipeline_dict(pipeline_id)
        self.id = pipeline_id
        self.url = pipeline_dict.get('url')
        self.short_url = self.__get_short_url(pipeline_dict.get('url'))
        self.description = pipeline_dict.get('description')
        self.vars = pipeline_dict.get('playbook_vars_template')
        self.profiles = self.__get_profiles(self.id, [*self.vars]) if with_profiles else None

    def get_profile(self, profile_id):
        return next((p for p in self.profiles if p.id == profile_id), None)

    def create_profile(self, profile_id, profile_data):
        if not self.get_profile(profile_id):
            Profiles(self.id, [*self.vars]).create_profile(profile_id)
            self.profiles = self.__get_profiles(self.id, [*self.vars])

        profile = self.get_profile(profile_id)
        profile.set_all(profile_data)
        profile.save()

        self.profiles = self.__get_profiles(self.id, [*self.vars])

        return self.get_profile(profile_id)

    def deploy_pipeline(self, profile_id):
        profile = self.get_profile(profile_id)
        return profile.deploy()

    def __get_pipeline_dict(self, pipeline_id):
        return SolidaConfigFile(yaml_file=settings.SOLIDA_CONFIG_FILE).get_pipelines_section().get(pipeline_id)

    def __get_short_url(self, pipeline_url):
        split_url = pipeline_url.split('/')
        short_url = os.path.join(split_url[-2], split_url[-1].split('.')[0])
        return short_url

    def __get_profiles(self, pipeline_id, pipeline_vars):
        return Profiles(pipeline_id, pipeline_vars).profiles


class Pipelines(object):
    def __init__(self, with_profiles=False):
        conf = SolidaConfigFile(yaml_file=settings.SOLIDA_CONFIG_FILE)
        self.pipelines = list()
        for pipeline_id, pipeline_dict in conf.get_pipelines_section().items():
            self.pipelines.append(Pipeline(pipeline_id=pipeline_id,
                                           pipeline_dict=pipeline_dict,
                                           with_profiles=with_profiles))

    def get(self):
        return self.pipelines

    def get_pipeline(self, pipeline_id):
        return next(p for p in self.pipelines if p.id == pipeline_id)

    def count_pipelines(self):
        return len(self.pipelines)

    def refresh_pipelines(self):
        return Solida().refresh()


