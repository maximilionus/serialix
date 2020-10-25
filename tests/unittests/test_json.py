import unittest

from configerz import JSON_Configuration

from ..fixtures import configuration_file_path,\
    default_configuration, default_configuration_file_path,\
    remove_temp_dir


class Test_DefaultFromDict(unittest.TestCase):
    def setUp(self):
        self.config_obj = JSON_Configuration(
            configuration_file_path,
            default_configuration,
            True
        )

    def tearDown(self):
        remove_temp_dir()

    def test_delete_file(self):
        result = self.config_obj.delete_file()
        self.assertEqual(result, True)

    def test_create_file(self):
        result = self.config_obj.create_file()
        self.assertEqual(result, True)

    def test_modify_commit_read(self):
        person_name = "Jeff"

        self.config_obj.Person_1.name = person_name
        self.config_obj.commit()

        file_dict = self.config_obj.fread_dict()

        self.assertEqual(
            file_dict["Person_1"]["name"],
            person_name
        )


class Test_DefaultFromFile(Test_DefaultFromDict):
    def setUp(self):
        self.config_obj = JSON_Configuration(
            configuration_file_path,
            default_configuration_file_path,
            True
        )
