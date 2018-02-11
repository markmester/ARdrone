import yaml
import os
import logging.config


def setup(path=None):
    """Helper for all project setup functions
    """
    if not path:
        path = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/config/config.yml"
    if not os.path.exists(path):
        print "Unable to find config! Exiting..."
        exit(1)

    setup_logging(path)

    return get_config(path)


def get_config(path):
    """Load project configuration
    """
    with open(path, "r") as f:
        return yaml.safe_load(f.read())


def setup_logging(path, level=logging.INFO):
    """Setup logging configuration
    """
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())['logging']
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=level)
