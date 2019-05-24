import os.path
import sys
import yaml

from components.logging import Logging


class YamlConfigFile(object):
    """
    Retrieve/Dump infrastructure configuration's details from/into a yaml file
    """
    def __init__(self, yaml_file, loglevel='INFO'):
        self.yaml_file = yaml_file
        self.logger = Logging(self.__class__.__name__, level=loglevel).get_logger()
        if os.path.isfile(self.yaml_file):
            self.conf = self.__load_config(self.yaml_file)
        else:
            self.logger.critical('{} not exists'.format(self.yaml_file))
            sys.exit()

    def __load_config(self, config_file):
        with open(config_file) as cfg:
            conf = yaml.load(cfg, Loader=yaml.FullLoader)
        return conf

    def __dump_config(self, config_file):
        with open(config_file, 'w') as f:
            yaml.dump(self.conf, f)

    def get_conf(self):
        return self.conf

    def set_conf(self, conf=None):
        self.conf = conf if conf else self.conf

    def get_section(self, section_label):
        if self.is_section_present(section_label):
            return self.conf[section_label]
        else:
            self.logger.warning('section {} not found'.format(section_label))
            return ''

    def set_section(self, section_label, section_dict):
        if not isinstance(section_dict, dict):
            self.logger.warning('section {} not well formatted'.format(section_label))

        if self.is_section_present(section_label):
            self.conf[section_label] = section_dict
        else:
            self.logger.warning('section {} not found'.format(section_label))

    def set_value(self, label, value):
        self.conf[label] = value

    def is_section_present(self, section_label):
        if section_label in self.conf:
            return True
        else:
            return False

    def dump(self, config_file=None):
        config_file = config_file if config_file else self.yaml_file
        self.__dump_config(config_file=config_file)


class SolidaConfigFile(YamlConfigFile):
    def __init__(self, yaml_file, loglevel='INFO'):
        YamlConfigFile.__init__(self, yaml_file, loglevel)

    def get_pipelines_section(self, label='pipelines'):
        return self.get_section(label)

    def get_remote_section(self, label='remote'):
        return self.get_section(label)

    def get_vars_section(self, label='default_vars'):
        return self.get_section(label)

    def add_new_pipeline(self, pipeline_dict):
        pipeline_section = self.get_pipelines_section()
        pipeline_section.update({pipeline_dict.get('label'): pipeline_dict})
        self.set_pipelines_section(pipeline_section)

    def set_pipelines_section(self, pipeline_section):
        self.set_section(section_label='pipelines', section_dict=pipeline_section)

    def __set_section(self, section):
        for k, v in section.items():
            self.set_value(k, v)


class ProfileConfigFile(YamlConfigFile):
    def __init__(self, yaml_file, loglevel='INFO'):
        YamlConfigFile.__init__(self, yaml_file, loglevel)

    def get_project_section(self):
        return dict(project_name=self.get_section('project_name'),
                    project_email_address=self.get_section('project_email_address'),
                    project_dir=self.get_section('project_dir'),
                    tmp_dir=self.get_section('tmp_dir'))

    def get_remote_section(self):
        return dict(host=self.get_section('host'),
                    remote_user=self.get_section('remote_user'),
                    connection=self.get_section('connection'))

    def set_remote_section(self, remote_section):
        self.__set_section(remote_section)

    def set_project_section(self, project_section):
        self.__set_section(project_section)

    def set_vars_section(self, vars_section):
        self.__set_section(vars_section)

    def __set_section(self, section):
        for k, v in section.items():
            self.set_value(k, v)
