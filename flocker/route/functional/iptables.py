# Copyright Hybrid Logic Ltd.  See LICENSE file for details.

"""
Testing tools related to iptables.
"""

from subprocess import PIPE, Popen, check_output

def preserve_iptables():
    """
    :py:func:`preserve_iptables` is a fixture which saves the current iptables
    configuration and restores it later.
    """
    rules = check_output([b"iptables-save"])
    def restore():
        process = Popen([b"iptables-restore"], stdin=PIPE)
        process.stdin.write(rules)
        process.stdin.close()
        exit_code = process.wait()
        if exit_code != 0:
            raise Exception(
                "Possibly failed to restore iptables configuration: %s" % (
                    exit_code,))
    return restore