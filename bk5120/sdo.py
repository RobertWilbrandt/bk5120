"""Implementation of the sdo console command"""
import argparse
import inspect

import cmd2

from .util import format_object_entry, int_with_radix, parse_object_entry


@cmd2.with_default_category("DS301")
class SdoCmd(cmd2.CommandSet):
    """Implementation of the sdo console command
    """

    def __init__(self, node):
        self._node = node

        super().__init__()

    def sdo_upload(self, args):
        """Transfer data from client to server

        Examples:
          sdo upload 0x1000    # Read device type
          sdo upload 0x6000 0  # Read number of digital inputs
        """
        entry = self._node.sdo[args.index]
        dict_entry = self._node.object_dictionary[args.index]
        if args.subindex is not None:
            entry = entry[args.subindex]
            dict_entry = dict_entry[args.subindex]

        formatted_entry = format_object_entry(entry.raw, dict_entry)
        self._cmd.poutput(formatted_entry)

    def sdo_download(self, args):
        """Transfer data from server to client

        Examples:
          sdo download 0x6200 0x1 0x3  # Turn two digital outputs on
        """
        entry = self._node.sdo[args.index]
        dict_entry = self._node.object_dictionary[args.index]
        if args.subindex is not None:
            entry = entry[args.subindex]
            dict_entry = dict_entry[args.subindex]

        parsed_value = parse_object_entry(args.value, dict_entry)
        entry.raw = parsed_value

    # Base parser
    sdo_parser = argparse.ArgumentParser()
    sdo_subparser = sdo_parser.add_subparsers(
        title="subcommands", help="Which SDO service to use"
    )

    # SDO upload parser
    sdo_upload_parser = sdo_subparser.add_parser(
        "upload",
        help="Transfer data from client to server",
        description=inspect.cleandoc(sdo_upload.__doc__),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sdo_upload_parser.set_defaults(func=sdo_upload)
    sdo_upload_parser.add_argument(
        "index", type=int_with_radix, help="Index of data to upload"
    )
    sdo_upload_parser.add_argument(
        "subindex", type=int_with_radix, nargs="?", help="Subindex of data to upload"
    )

    # SDO download parser
    sdo_download_parser = sdo_subparser.add_parser(
        "download",
        help="Transfer data from server to client",
        description=inspect.cleandoc(sdo_download.__doc__),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sdo_download_parser.set_defaults(func=sdo_download)
    sdo_download_parser.add_argument(
        "index", type=int_with_radix, help="Index to download to"
    )
    sdo_download_parser.add_argument(
        "subindex", type=int_with_radix, nargs="?", help="Subindex to download to"
    )
    sdo_download_parser.add_argument("value", help="Value to download to device")

    @cmd2.with_argparser(sdo_parser)
    def do_sdo(self, args):
        """Directly exchange data with client using SDO services"""
        func = getattr(args, "func", None)
        if func is not None:
            func(self, args)
        else:
            self._cmd.perror("Invalid command")
            self._cmd.do_help("sdo")
