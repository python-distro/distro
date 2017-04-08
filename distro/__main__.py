import argparse
import json
import logging
import sys
from . import name, info, version, codename


def main():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler(sys.stdout))

    parser = argparse.ArgumentParser(description="Linux distro info tool")
    parser.add_argument(
        '--json',
        '-j',
        help="Output in machine readable format",
        action="store_true")
    args = parser.parse_args()

    if args.json:
        logger.info(json.dumps(info(), indent=4, sort_keys=True))
    else:
        logger.info('Name: %s', name(pretty=True))
        distribution_version = version(pretty=True)
        logger.info('Version: %s', distribution_version)
        distribution_codename = codename()
        logger.info('Codename: %s', distribution_codename)


if __name__ == '__main__':
    main()