"""Small console to test the BK5120 CANopen bus coupler"""
import cmd2


def split_args(args):
    """Split shell arguments into usable parts

    :param args: Raw arguments
    :type args: list
    """
    return [i for i in args.split(" ") if i != ""]


class Console(cmd2.Cmd):
    """Minimal BK5120 control shell

    :param network: CANopen network to use
    :type network: canopen.Network
    :param node: CANopen node to control
    :type node: canopen.Node
    """

    # pylint: disable=no-self-use

    def __init__(self, network, node):
        self._network = network
        self._node = node

        super().__init__(allow_cli_args=False)

    def help_type(self):
        """Print help information for 'type' command
        """
        print("Read device type information using SDO")

    def do_type(self, raw_args):
        """Implementation of 'type' command

        :param raw_args: Command arguments
        :type raw_args: list
        """
        args = split_args(raw_args)

        if len(args) == 0:
            device_type = self._node.sdo[0x1000].raw

            if bool(0x800000 & device_type):
                pdo_mappings = "Device specific"
            else:
                pdo_mappings = "Pre-defined generic"

            print(f"Raw device type entry:  0x{device_type:08x}")
            print(f"  Device profile:       {((1<<16)-1) & device_type}")
            print(f"  Digital input(s):     {bool(0x10000 & device_type)}")
            print(f"  Digital output(s):    {bool(0x20000 & device_type)}")
            print(f"  Analogue input(s):    {bool(0x40000 & device_type)}")
            print(f"  Analogue output(s):   {bool(0x80000 & device_type)}")
            print(f"  PDO mappings:         {pdo_mappings}")

        else:
            print("Usage: type")

    def do_device(self, raw_args):
        """Implementation of 'device' command

        :param raw_args: Command arguments
        :type raw_args: list
        """
        args = split_args(raw_args)

        if len(args) == 0:
            man_dev_name = self._node.sdo[0x1008].raw
            man_hw_ver = self._node.sdo[0x1009].raw
            man_sw_ver = self._node.sdo[0x100A].raw

            print(f"Manufacturer device name:       {man_dev_name}")
            print(f"Manufacturer hardware version:  {man_hw_ver}")
            print(f"Manufacturer software version:  {man_sw_ver}")

        else:
            print("Usage: device")

    def help_device(self):
        """Print help information for 'device' command
        """
        print("Read manufacturer device information")

    def help_sdo(self):
        """Print help information for 'sdo' command
        """
        print("Directly access object dictionary using SDOs")
        print("")
        print("Upload:")
        print("  sdo upload <address> [<subaddress>]")
        print("Download:")
        print("  sdo download <address> [<subaddress>] <value>")
        print("")
        print("Examples:")
        print("  sdo upload 0x1000            # Read device type")
        print("  sdo upload 0x6000 0          # Read number of digital inputs")
        print("  sdo download 0x6200 0x1 0x3  # Turn two digital outputs on")

    def do_sdo(self, raw_args):
        """Implementation of 'sdo' command

        :param raw_args: Command argument
        :type args: list
        """
        args = split_args(raw_args)

        # Upload
        if len(args) > 1 and len(args) <= 3 and args[0] == "upload":
            entry = self._node.sdo[int(args[1], 0)]
            if len(args) == 3:
                entry = entry[int(args[2], 0)]

            print(f"0x{entry.raw:x}")
            return False

        # Download
        if len(args) > 2 and len(args) <= 4 and args[0] == "download":
            entry = self._node.sdo[int(args[1], 0)]
            value = args[2]

            if len(args) == 4:
                entry = entry[int(args[2], 0)]
                value = args[3]

            entry.raw = int(value, 0)
            return False

        print("Invalid command. Check ?sdo to see all valid SDO commands")
        return False

    def help_nmt(self):
        """Print help information for the 'nmt' command
        """
        print("Directly interact with the NMT protocol")
        print("")
        print("Enter a different NMT state:")
        print("  nmt start")
        print("  nmt stop")
        print("  nmt enter pre-operational")
        print("  nmt reset node")
        print("  nmt reset communication")

    def do_nmt(self, raw_args):
        """Implementation of 'nmt' command

        :param raw_args: Commnd arguments
        :type raw_args: list
        """
        args = split_args(raw_args)
        if len(args) == 1 and args[0] == "start":
            self._node.nmt.send_command(0x1)
        elif len(args) == 1 and args[0] == "stop":
            self._node.nmt.send_command(0x2)
        elif len(args) == 2 and args[0] == "enter" and args[1] == "pre-operational":
            self._node.nmt.send_command(0x80)
        elif len(args) == 2 and args[0] == "reset" and args[1] == "node":
            self._node.nmt.send_command(0x81)
        elif len(args) == 2 and args[0] == "reset" and args[1] == "communication":
            self._node.nmt.send_command(0x82)
        else:
            print("Invalid argument. Check ?nmt to see all valid NMT commands")

    def help_quit(self):
        """Print help information for 'quit' command
        """
        print("Exit this shell")

    def do_quit(self, _):
        """Implementation of 'quit' command, exiting the shell

        :return: True, as this should exit the shell
        :rtype: bool
        """
        return True
