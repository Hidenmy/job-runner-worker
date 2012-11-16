import unittest2 as unittest

from mock import Mock, patch

from job_runner_worker.config import get_config_parser, setup_log_handler


class ModuleTestCase(unittest.TestCase):
    """
    Tests for :py:mod:`job_runner_worker.config`.
    """
    @patch('job_runner_worker.config.ConfigParser')
    @patch('job_runner_worker.config.os')
    def test_get_config_parser(self, os, ConfigParser):
        """
        Test :py:func:`.get_config_parser`.
        """
        os.environ = {'SETTINGS_PATH': '/path/to/settings'}

        config_mock = Mock()
        ConfigParser.ConfigParser.return_value = config_mock

        config = get_config_parser()

        ConfigParser.ConfigParser.assert_called_once_with({
            'log_level': 'info',
        })
        config_mock.read.assert_called_once_with('/path/to/settings')
        self.assertEqual(config_mock, config)

    @patch('job_runner_worker.config.logging')
    def test_setup_log_handler(self, logging):
        """
        Test :func:`.setup_log_handler`.
        """
        setup_log_handler('INFO')

        logging.basicConfig.assert_called_once_with(
            level=logging.INFO,
            format='%(levelname)s - %(asctime)s - %(name)s: %(message)s',
        )