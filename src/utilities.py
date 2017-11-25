import yaml
import os
import logging.config


def get_config(path):
    """Load project configuration
    """
    with open(path, "r") as f:
        return yaml.safe_load(f.read())


def setup_logging(default_path='config/config.yml', default_level=logging.INFO):
    """Setup logging configuration
    """
    path = default_path
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())['logging']
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
