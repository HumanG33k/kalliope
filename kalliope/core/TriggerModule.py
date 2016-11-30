import os

import logging

from kalliope.core.ConfigurationManager import utils

logging.basicConfig()
logger = logging.getLogger("kalliope")


class TriggerModule(object):
    """
    Mother class of a trigger object
    """

    def __init__(self):
        super(TriggerModule, self).__init__()

    @staticmethod
    def get_file_from_path(file_path):
        """
        Trigger can be based on a model file, or other file.
        If a file is precised in settings, the path can be relative or absolute.
        If the path is absolute, there is no problem when can try to load it directly
        If the path is relative, we need to test the get the full path of the file in the following order:
            - from the current directory where kalliope has been called. Eg: /home/me/Documents/kalliope_config
            - from /etc/kalliope
            - from the root of the project. Eg: /usr/local/lib/python2.7/dist-packages/kalliope-version/kalliope/<file_path>

        :return: absolute path
        """
        if not os.path.isabs(file_path):
            path_order = {
                1: os.getcwd() + os.sep + file_path,
                2: "/etc/kalliope" + os.sep + file_path,
                3: utils.get_root_kalliope_path() + os.sep + file_path
            }

            for key in sorted(path_order):
                file_path_to_test = path_order[key]
                logger.debug("Trigger: Try to load given file from %s: %s" % (key, file_path_to_test))
                if os.path.isfile(file_path_to_test):
                    logger.debug("Trigger: given path found in %s" % file_path_to_test)
                    return file_path_to_test

        logger.debug("Trigger file to load will be %s" % file_path)
        return file_path
