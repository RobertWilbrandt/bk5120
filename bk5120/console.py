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

    def __init__(self, network, node, *args, **kwargs):
        self._network = network
        self._node = node

        super().__init__(allow_cli_args=False, *args, **kwargs)

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
