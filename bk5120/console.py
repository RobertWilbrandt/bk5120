"""Small console to test the BK5120 CANopen bus coupler"""
import cmd2


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
