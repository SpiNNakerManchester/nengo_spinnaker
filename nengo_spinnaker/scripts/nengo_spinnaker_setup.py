"""A script which helps users create their nengo_spinnaker config file."""

import argparse

from nengo_spinnaker.utils.paths import nengo_spinnaker_rc

from rig import wizard

import os


CONFIG_TEMPLATE = """\
### SpiNNaker system configuration.
# File automatically generated by nengo_spinnaker_setup.
[spinnaker_machine]
hostname: {hostname}
"""


def generate_config_file(filename, ip_address):
    """Generate a new config file with the specified filename and
    parameters.
    """
    try:
        os.makedirs(os.path.dirname(filename))
    except (IOError, OSError):
        # Directory already created, good job!
        pass

    with open(filename, "w") as f:
        f.write(CONFIG_TEMPLATE.format(
            hostname=ip_address,
        ))


def main(args=None):
    parser = argparse.ArgumentParser(
        description="Interactive tool for creating a nengo_spinnaker "
                    "config file.")

    file_group = parser.add_mutually_exclusive_group()
    file_group.add_argument("--user", "-u", dest="file",
                            const="user", action="store_const",
                            help="Create a user-specific config file "
                                 "(default).")
    file_group.add_argument("--project", "-p", dest="file",
                            const="project", action="store_const",
                            help="Create a project-specific config file in "
                                 "the current directory.")
    file_group.set_defaults(file="user")

    parser.add_argument("--force", "-f", action="store_true",
                        help="Overwrite an existing config file.")

    args = parser.parse_args(args)

    filename = nengo_spinnaker_rc[args.file]

    if not args.force and os.path.isfile(filename):
        print("Config file {} already exists. Use --force to "
              "overwrite.".format(filename))
        return 1

    resp = wizard.cli_wrapper(wizard.ip_address_wizard())

    if resp is None:
        return 1
    else:
        generate_config_file(filename, **resp)
        print("Successfully created config file in {}".format(filename))
        return 0


if __name__ == "__main__":  # pragma: no cover
    import sys
    sys.exit(main())
