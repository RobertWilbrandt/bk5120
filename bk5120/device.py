"""Implementation of the device console command"""
import argparse

import cmd2


@cmd2.with_default_category("High-level")
class DeviceCmd(cmd2.CommandSet):
    """Implementation of the device console command
    """

    def __init__(self, node):
        self._node = node

        super().__init__()

    def device_type(self, args):  # pylint: disable=unused-argument
        """Read device type information from device
        """
        device_type = self._node.sdo[0x1000].raw

        if bool(0x800000 & device_type):
            pdo_mappings = "Device specific"
        else:
            pdo_mappings = "Pre-defined generic"

        self._cmd.poutput(f"Raw device type entry:  0x{device_type:08x}")
        self._cmd.poutput(f"  Device profile:       {((1<<16)-1) & device_type}")
        self._cmd.poutput(f"  Digital input(s):     {bool(0x10000 & device_type)}")
        self._cmd.poutput(f"  Digital output(s):    {bool(0x20000 & device_type)}")
        self._cmd.poutput(f"  Analogue input(s):    {bool(0x40000 & device_type)}")
        self._cmd.poutput(f"  Analogue output(s):   {bool(0x80000 & device_type)}")
        self._cmd.poutput(f"  PDO mappings:         {pdo_mappings}")

    def device_name(self, _):
        """Read device name from device
        """
        man_dev_name = self._node.sdo[0x1008].raw
        self._cmd.poutput(f"Manufacturer device name:  {man_dev_name}")

    def device_version(self, _):
        """Read device version from device
        """
        man_hw_version = self._node.sdo[0x1009].raw
        man_sw_version = self._node.sdo[0x100A].raw

        self._cmd.poutput(f"Manufacturer hardware version:  {man_hw_version}")
        self._cmd.poutput(f"Manufacturer software version:  {man_sw_version}")

    # Base parser
    device_parser = argparse.ArgumentParser()
    device_subparsers = device_parser.add_subparsers(
        title="subcommands", help="What kind of device information to query"
    )

    # Device type parser
    device_type_parser = device_subparsers.add_parser(
        "type",
        help="Read device type information from device",
        description=device_type.__doc__,
    )
    device_type_parser.set_defaults(func=device_type)

    # Device name parser
    device_name_parser = device_subparsers.add_parser(
        "name", help="Read device name from device", description=device_name.__doc__
    )
    device_name_parser.set_defaults(func=device_name)

    # Device version parser
    device_version_parser = device_subparsers.add_parser(
        "version",
        help="Read device version from device",
        description=device_name.__doc__,
    )
    device_version_parser.set_defaults(func=device_version)

    @cmd2.with_argparser(device_parser)
    def do_device(self, args):
        """Read device specific information from device"""
        func = getattr(args, "func", None)
        if func is not None:
            func(self, args)
        else:
            self._cmd.perror("Invalid command")
            self._cmd.do_help("device")
