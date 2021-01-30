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

    #
    # NMT service implementation
    #

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
        """Use one of the NMT services to change the NMT state
        """
        self.NMT_SERVICES[args.service](self, args)

    #
    # NMT node-guarding implementation
    #

    def nmt_node_guarding_start(self, args):
        """Start the node-guarding error control protocol

        This will do two things:
        - Set up node-guarding parameters via SDO
        - Start sending periodic node-guarding messages
        """
        guard_time_in_s = args.guard_time / 1000.0
        self._node.nmt.start_node_guarding(guard_time_in_s)

        self._node.sdo[0x100C].raw = args.guard_time
        self._node.sdo[0x100D].raw = args.life_time_factor

        self._cmd.pfeedback(
            f"Started NMT node guarding with guard time {guard_time_in_s}s and node "
            f"life time {args.life_time_factor*guard_time_in_s}s"
        )

    def nmt_node_guarding_stop(self, _):
        """Stop the node-guarding error control protocol

        This will do two things:
        - Disable node-guarding via SDO
        - Stop sending periodic node-guarding messages
        """
        self._node.sdo[0x100C].raw = 0x0
        self._node.sdo[0x100D].raw = 0x0

        self._node.nmt.stop_node_guarding()

        self._cmd.pfeedback("Stopped node guarding")

    def nmt_node_guarding(self, args):
        """Configure and control the NMT node guarding error control protocol
        """
        subfunc = getattr(args, "subfunc", None)
        if subfunc is not None:
            subfunc(self, args)
        else:
            self._cmd.perror("Invalid command")
            self._cmd.do_help("nmt node-guarding")

    #
    # Command parser setup
    #

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

    # NMT node guarding parser
    nmt_node_guarding_parser = nmt_subparsers.add_parser(
        "node-guarding",
        help="Configure and control the NMT node guarding error control protocol",
        description=inspect.cleandoc(nmt_node_guarding.__doc__),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    nmt_node_guarding_parser.set_defaults(func=nmt_node_guarding)
    nmt_node_guarding_subparsers = nmt_node_guarding_parser.add_subparsers(
        title="subcommands",
        help="What to do with the NMT node guarding error control protocol",
    )

    # NMT node guarding start sub-parser
    nmt_node_guarding_start_parser = nmt_node_guarding_subparsers.add_parser(
        "start",
        help="Start the NMT node guarding error control protocol",
        description=inspect.cleandoc(nmt_node_guarding_start.__doc__),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    nmt_node_guarding_start_parser.set_defaults(subfunc=nmt_node_guarding_start)
    nmt_node_guarding_start_parser.add_argument(
        "guard_time",
        nargs="?",
        type=int,
        default=100,
        help="Period of node guard RTR in ms",
    )
    nmt_node_guarding_start_parser.add_argument(
        "life_time_factor",
        nargs="?",
        type=int,
        default=5,
        help="Number of anticipated node guarding RTRs without request after which an "
        "error should be raised",
    )

    # NMT node guarding stop sub-parser
    nmt_node_guarding_stop_parser = nmt_node_guarding_subparsers.add_parser(
        "stop",
        help="Stop the NMT node guarding error control protocol",
        description=inspect.cleandoc(nmt_node_guarding_stop.__doc__),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    nmt_node_guarding_stop_parser.set_defaults(subfunc=nmt_node_guarding_stop)

    @cmd2.with_argparser(nmt_parser)
    def do_nmt(self, args):
        """Interact with the NMT protocol"""
        func = getattr(args, "func", None)
        if func is not None:
            func(self, args)
        else:
            self._cmd.perror("Invalid command")
            self._cmd.do_help("nmt")
