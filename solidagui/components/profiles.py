from django.conf import settings
from components.configs import ProfileConfigFile
from components.configs import SolidaConfigFile
from components.solida import Solida

import os


class Profile(object):
    def __init__(self, pipeline_id, profile_id, pipeline_vars=None):
        profile = self.__get_profile(pipeline_id, profile_id)

        self.id = profile_id
        self.pipeline_id = pipeline_id
        self.remote_section = self.__retrieve(profile, profile.get_remote_section())
        self.project_section = self.__retrieve(profile, profile.get_project_section())
        self.vars_section = self.__retrieve(profile, pipeline_vars)

    def set_all(self, bulk):
        self.set_remote_section(bulk)
        self.set_project_section(bulk)
        self.set_vars_section(bulk)

    def set_remote_section(self, remote_section):
        for k, v in remote_section.items():
            if k in self.remote_section:
                self.remote_section[k]['value'] = remote_section[k]

    def set_project_section(self, project_section):
        for k, v in project_section.items():
            if k in self.project_section:
                self.project_section[k]['value'] = project_section[k]

    def set_vars_section(self, vars_section):
        for k, v in vars_section.items():
            if k in self.vars_section:
                self.vars_section[k]['value'] = vars_section[k]

    def save(self):
        config_file = self.__get_config_file(self.pipeline_id, self.id)

        profile = ProfileConfigFile(yaml_file=config_file)
        profile.set_remote_section(self.__revert(self.remote_section))
        profile.set_project_section(self.__revert(self.project_section))
        profile.set_vars_section(self.__revert(self.vars_section))
        profile.dump()

    def deploy(self):
        solida = Solida()
        return solida.deploy(pipeline_id=self.pipeline_id,
                             profile_id=self.id,
                             host=self.remote_section['host']['value'],
                             user=self.remote_section['remote_user']['value'],
                             connection=self.remote_section['connection']['value'])

    def __get_profile(self, pipeline_id, profile_id):
        config_file = self.__get_config_file(pipeline_id, profile_id)

        return ProfileConfigFile(yaml_file=config_file)

    def __retrieve(self, profile, to_be_retrieved):
        ret = dict()
        if to_be_retrieved:
            for k in to_be_retrieved:
                ret[k] = dict(label=k.replace('_', ' ').title(), value=profile.get_section(k))
        return ret

    def __revert(self, to_be_reverted):
        ret = dict()
        for k, v in to_be_reverted.items():
            ret.update({k: v.get('value')})
        return ret

    def __get_config_file(self, pipeline_id, profile_id):
        return os.path.join(settings.SOLIDA_PROFILES_ROOT,
                            pipeline_id,
                            profile_id + ".yaml")


class Profiles(object):
    def __init__(self, pipeline_id, pipeline_vars):
        self.pipeline_id = pipeline_id
        self.profiles_root = os.path.join(settings.SOLIDA_PROFILES_ROOT, self.pipeline_id)
        self.__bootstrap()
        self.profiles = self.__get_profiles(pipeline_vars)

    def __bootstrap(self):
        if not os.path.exists(self.profiles_root):
            self.create_profile(settings.SOLIDA_PROFILE_NAME)

    def create_profile(self, profile_id):
        conf = SolidaConfigFile(yaml_file=settings.SOLIDA_CONFIG_FILE)
        solida = Solida()
        solida.create_profile(pipeline_id=self.pipeline_id,
                              profile_id=profile_id)
        profile = Profile(self.pipeline_id, settings.SOLIDA_PROFILE_NAME)
        remote_section = dict()
        for k, v in conf.get_remote_section().items():
            remote_section.update({k.replace('-', '_'): v})
        profile.set_remote_section(remote_section)
        profile.save()

    def __get_profiles(self, pipeline_vars):
        profiles = list()
        (_, _, filenames) = next(os.walk(self.profiles_root))
        for config_file in filenames:
            profile_id = os.path.splitext(os.path.basename(config_file))[0]
            profiles.append(Profile(self.pipeline_id, profile_id, pipeline_vars))
        return profiles

    def get_profile(self, profile_id):
        return next(p for p in self.profiles if p.id == profile_id)

    def count_profiles(self):
        return len(self.profiles)
