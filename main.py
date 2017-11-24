from utilities import get_config, setup_logging
import logging


setup_logging()
ARdrone_logger = logging.getLogger("ARdrone-controller")

config = get_config("config/config.yml")


if __name__ == '__main__':
    logging.info("printing config...")  # root logger
    print(config)
    ARdrone_logger.info("done")  # module specific logger
