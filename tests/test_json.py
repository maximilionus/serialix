from configerz import JSON_Configuration

from .core import BaseConfigTest, configuration_file_path,\
    default_configuration_dict, default_cfg_json_path, remove_temp_dir


def teardown_module():
    remove_temp_dir()


class Test_Create_DefDict(BaseConfigTest):
    """
    Create configuration file on `configuration_file_path`
    and get default config values from `default_configuration_dict`
    """
    def setup(self):
        self.config_obj = JSON_Configuration(
            configuration_file_path,
            default_configuration_dict,
            True
        )


class Test_Create_DefPath(BaseConfigTest):
    """
    Read existing file on `configuration_file_path`
    and get default config values from file on `default_cfg_json_path`
    """
    def setup(self):
        self.config_obj = JSON_Configuration(
            configuration_file_path,
            default_cfg_json_path,
            True
        )