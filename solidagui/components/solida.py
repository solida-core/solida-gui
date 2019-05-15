import subprocess
import shlex

from components.logging import Logging


class Solida(object):
    def __init__(self):
        self.launcher = Launcher()

    def create_profile(self, pipeline_id, profile_id):
        return self.launcher.create_profile(pipeline_id=pipeline_id,
                                            profile_id=profile_id)

    def deploy(self, pipeline_id, profile_id, host, user, connection):
        return self.launcher.deploy_project(pipeline_id=pipeline_id,
                                            profile_id=profile_id,
                                            host=host,
                                            user=user,
                                            connection=connection)

    def refresh(self):
        return self.launcher.refresh()


class Launcher(object):
    def __init__(self, loglevel='INFO'):
        self.logger = Logging(self.__class__.__name__, level=loglevel).get_logger()

    def create_profile(self, pipeline_id, profile_id):
        params = dict(pipeline_id=pipeline_id,
                      profile_id=profile_id)
        cmd = self.__get_cmd(self.create_profile.__name__, params)
        return self.__run(cmd=cmd)

    def deploy_project(self, pipeline_id, profile_id, host, user, connection):
        params = dict(pipeline_id=pipeline_id,
                      profile_id=profile_id,
                      host=host,
                      user=user,
                      connection=connection)
        cmd = self.__get_cmd(self.deploy_project.__name__, params)
        return self.__run(cmd=cmd)

    def refresh(self):
        cmd = self.__get_cmd(self.refresh.__name__)
        return self.__run(cmd=cmd)

    def __get_cmd(self, cmd, params=dict()):
        cmds = dict(
            create_profile=["solida setup",
                            "-l {}".format(params.get('pipeline_id')),
                            "-p {}".format(params.get('profile_id')),
                            "--create-profile"],

            deploy_project=["solida setup",
                            "-l {}".format(params.get('pipeline_id')),
                            "-p {}".format(params.get('profile_id')),
                            "--deploy",
                            "--host {}".format(params.get('host')),
                            "--remote-user {}".format(params.get('user')),
                            "--connection {}".format(params.get('connection'))],

            refresh=['solida refresh'],
        )

        return cmds.get(cmd)

    def __run(self, cmd):
        try:
            # subprocess.check_output(cmd)
            cmd = shlex.split(' '.join(cmd))
            process = subprocess.Popen(cmd,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT)
            std_data = process.communicate()
            exit_code = process.wait()
            return dict(stdout_data=std_data[0],
                        stderr_data=std_data[1],
                        exit_code=exit_code)

        except subprocess.CalledProcessError as e:
            self.logger.warining(e)
            if e.output:
                self.logger.warning("command output: %s", e.output)
            else:
                self.logger.warning("no command output available")
            return False
