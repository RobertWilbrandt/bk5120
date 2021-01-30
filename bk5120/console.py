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
