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

    def __init__(self, app_name, root_dir, path=None):
        """
            @param root_dir: path to server file or dir that will be using the config.
        """
        self.app_name = app_name

        root_dir = os.path.realpath(root_dir)
        if os.path.isfile(root_dir):
            root_dir = os.path.dirname(root_dir)
        self.dir = root_dir
        self.custom_path = path


    @property
    def user_path(self):
        """
            Constructs a path to the user's config file for this application under
        /home/USERNAME/.config/APP_NAME.conf
        """
        return os.path.join(os.path.expanduser('~'), '.config', self.app_name) + '.conf'


    @property
    def global_path(self):
        """
            Construct a path to a global config file of the application:
        /etc/aap_name.conf
        """
        return os.path.join('/etc/', self.app_name) + '.conf'


    @property
    def inproject_path(self):
        """
            Constructs a path to a config file in the directory of running file:
        /PATH_TO_THIS_APP/server.conf
        """
        config_path = os.path.join(self.dir, 'server.conf')
        return config_path


    @property
    def inproject_name_path(self):
        """
            Constructs a path to a config file in the directory of running file:
        /PATH_TO_THIS_APP/APP_NAME.conf
        """
        config_path = os.path.join(self.dir, '%s.conf' % self.app_name)
        return config_path


    @property
    def priority_path(self):
        for cfg_path in self.cfg_priority_order:
            if cfg_path is None:
                continue

            if os.path.exists(cfg_path):
                return cfg_path
        return None


    @property
    def cfg_priority_order(self):
        priority_order = [
            self.user_path,
            self.global_path,
            self.inproject_name_path,
            self.inproject_path,
        ]

        if self.custom_path is not None:
            priority_order.insert(0, self.custom_path)

        return priority_order