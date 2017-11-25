import logging

from src.utilities import get_config, setup_logging
from src.ARDrone import ARDrone
setup_logging()
ARdrone_logger = logging.getLogger("ARdrone-controller")

config = get_config("config/config.yml")


if __name__ == '__main__':
    logging.info("Starting drone test...")  # root logger
    drone = ARDrone(drone_config=config)
    drone.command(config['commands']['AT_REF']['takeoff'], "1")
