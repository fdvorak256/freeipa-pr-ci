import os
from task import PopenTask, FallibleTask, TaskException


class AnsibleFixKeysPermissions(FallibleTask):
    def __init__(self, directory='../keys', **kwargs):
        super(AnsibleFixKeysPermissions, self).__init__(**kwargs)
        self.directory = directory

    def _run(self):
        try:
            for file_ in os.listdir(self.directory):
                if not file_.endswith(".pub"):
                    os.chmod(os.path.join(self.directory, file_), 0600)
        except (IOError, OSError):
            raise TaskException(self, 'unable to fix key permissions')


class AnsiblePlaybook(PopenTask):
    def __init__(self, playbook=None, inventory='hosts', extra_vars=None,
                 verbosity=None, **kwargs):
        self.extra_vars = extra_vars
        self.playbook = playbook
        self.inventory = inventory
        self.extra_vars = extra_vars
        self.verbosity = verbosity

        if self.playbook is None:
            raise TaskException(self, 'playbook is required')

        cmd = [
            "ansible-playbook",
            "-i", self.inventory,
            self.playbook]

        if self.extra_vars is not None:
            for name, value in self.extra_vars.items():
                cmd[3:3] = ['-e', '{name}={value}'.format(
                    name=name,
                    value=value)]

        if self.verbosity is not None:
            cmd.append('-{verbosity}'.format(verbosity=self.verbosity))

        super(AnsiblePlaybook, self).__init__(cmd, **kwargs)

