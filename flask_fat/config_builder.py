import os


class ConfigBuilder:
    """
     This object used by the APIBaseline and helps find the config file in the
    several "expected" locations, such as /etc/, $HOME/.config/ or in the project
    folder itself. It also picks the first found config based of the location
    priority: 1) local at $HOME/.config/, 2) global at /etc/ 3) project folder.

    However, this most likely will be ignored if the user sends a config path
    from the command line directly.
    """

    def __init__(self, app_name, running_file):
        self.app_name = app_name
        self.running_file = running_file


    @property
    def user_cfg_path(self):
        """
            Constructs a path to the user's config file for this application under
        /home/USERNAME/.config/APP_NAME.conf
        """
        return os.path.join(os.path.expanduser('~'), '.config', self.app_name) + '.conf'


    @property
    def global_cfg_path(self):
        """
            Construct a path to a global config file of the application:
        /etc/aap_name.conf
        """
        return os.path.join('/etc/', self.app_name) + '.conf'


    @property
    def inproject_cfg_path(self):
        """
            Constructs a path to a config file in the directory of running file:
        /PATH_TO_THIS_APP/config.conf
        """
        config_path = os.path.realpath(self.running_file)
        config_path = os.path.dirname(config_path)
        config_path = os.path.join(config_path, 'config.conf')
        return config_path


    @property
    def priority_cfg_path(self):
        for cfg_path in self.cfg_priority_order:
            if os.path.exists(cfg_path):
                return cfg_path
        return None


    @property
    def cfg_priority_order(self):
        priority_order = [
            self.user_cfg_path,
            self.global_cfg_path,
            self.inproject_cfg_path,
        ]
        return priority_order