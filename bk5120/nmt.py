"""Implementation of the nmt console command"""
import argparse
import inspect

import cmd2


@cmd2.with_default_category("DS301")
class NmtCmd(cmd2.CommandSet):
    """Implementation of the nmt console command
    """

    def __init__(self, node):
        self._node = node

        super().__init__()

    def nmt_service_start(self, _):
        """Change the NMT state by using the 'start' service
        """
        self._node.nmt.send_command(0x1)

    def nmt_service_stop(self, _):
        """Change the NMT state by using the 'stop' service
        """
        self._node.nmt.send_command(0x2)

    def nmt_service_enter_preoperational(self, _):
        """Change the NMT state by using the 'enter pre-operational' service
        """
        self._node.nmt.send_command(0x80)

    def nmt_service_reset_node(self, _):
        """Change the NMT state by using the 'reset node' service
        """
        self._node.nmt.send_command(0x81)

    def nmt_service_reset_communication(self, _):
        """Change the NMT state by using the 'reset communication' service
        """
        self._node.nmt.send_command(0x82)

    NMT_SERVICES = {
        "start": nmt_service_start,
        "stop": nmt_service_stop,
        "enter-pre-operational": nmt_service_enter_preoperational,
        "reset-node": nmt_service_reset_node,
        "reset-communication": nmt_service_reset_communication,
    }

    def nmt_service(self, args):
        """Use on of the NMT services to change the NMT state
        """
        self.NMT_SERVICES[args.service](self, args)

    # Base parser
    nmt_parser = argparse.ArgumentParser()
    nmt_subparsers = nmt_parser.add_subparsers(
        title="subcommands", help="What to do with NMT protocol"
    )

    # NMT service parser
    nmt_service_parser = nmt_subparsers.add_parser(
        "service",
        help="Use one of the NMT services to change the NMT state",
        description=inspect.cleandoc(nmt_service.__doc__),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    nmt_service_parser.set_defaults(func=nmt_service)
    nmt_service_parser.add_argument(
        "service", choices=NMT_SERVICES.keys(), help="Which NMT service to call"
    )

    @cmd2.with_argparser(nmt_parser)
    def do_nmt(self, args):
        """Interact with the NMT protocol"""
        func = getattr(args, "func", None)
        if func is not None:
            func(self, args)
        else:
            self._cmd.perror("Invalid command")
            self._cmd.do_help("nmt")
