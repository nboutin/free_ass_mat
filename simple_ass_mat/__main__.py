"""
:author Nicolas Boutin
:date 2023-07-04
"""
# pylint: disable=logging-fstring-interpolation

import logging
# import yaml

# from simple_ass_mat.controller import factory

__NAME = "Free AssMat"

logger = logging.getLogger(__name__)


def main():
    """main"""
    logging.basicConfig(level=logging.DEBUG)
    logger.info(f"Running {__NAME}")

    # with open("data.yml", "r", encoding="utf-8") as file:
    #     data = yaml.safe_load(file)


if __name__ == "__main__":
    main()
