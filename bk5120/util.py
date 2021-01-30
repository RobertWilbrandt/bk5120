"""Utility methods for CANopen based console
"""
# pylint: disable=fixme


def int_with_radix(string):
    """Parse integer with or without a base prefix

    :param string: String representation of integer
    :type string: str
    :return: Parsed integer
    :rtype: int
    :raise ValueError: If string is no valid integer representation
    """
    return int(string, 0)


def parse_object_entry(string, dict_entry):
    """Parse string according to a dictionary entry type

    :param string: String representation of object entry
    :type string: str
    :param dict_entry: Corresponding object dictionary entry
    :type dict_entry: canopen.objectdictionary.Variable
    :return: Correctly parsed object entry
    :rtype: Depending on object entry type
    """
    # TODO: Handle all data entry types from 7.4.7.1
    if dict_entry.data_type == 0x09:
        return str(string)

    return int(string, 0)


def format_object_entry(entry, dict_entry):
    """Format an object dictionary entry according to its type

    :param entry: Object dictionary entry
    :type entry: Depending on entry type
    :param dict_entry: Corresponding object dictionary entry
    :type dict_entry: canopen.objectdictionary.Variable
    :return: Nicely formatted object entry
    :rtype: str
    """
    # TODO: Handle all data entry types from 7.4.7.1
    if dict_entry.data_type == 0x09:
        return str(entry)

    return f"0x{entry:x}"
