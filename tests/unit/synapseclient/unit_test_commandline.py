"""Test the Synapse command line client.

"""

from nose.tools import assert_equal, assert_true, assert_false
from mock import patch, Mock

import synapseutils
import synapseclient.__main__ as cmdline
from tests import unit


def setup(module):
    module.syn = unit.syn


def test_command_sync():
    """Test the sync function.

    Since this function only passes argparse arguments for the sync subcommand
    straight to `synapseutils.sync.syncToSynapse`, the only tests here are for
    the command line arguments provided and that the function is called once.

    """

    parser = cmdline.build_parser()
    args = parser.parse_args(['sync', '/tmp/foobarbaz.tsv'])

    assert_equal(args.manifestFile, '/tmp/foobarbaz.tsv')
    assert_equal(args.dryRun, False)
    assert_equal(args.sendMessages, False)
    assert_equal(args.retries, 4)

    with patch.object(synapseutils, "syncToSynapse") as mockedSyncToSynapse:
        cmdline.sync(args, syn)
        mockedSyncToSynapse.assert_called_once_with(syn,
                                                    manifestFile=args.manifestFile,
                                                    dryRun=args.dryRun,
                                                    sendMessages=args.sendMessages,
                                                    retries=args.retries)


def test_get_multi_threaded_flag():
    """Test the sync function.

    Since this function only passes argparse arguments for the sync subcommand
    straight to `synapseutils.sync.syncToSynapse`, the only tests here are for
    the command line arguments provided and that the function is called once.

    """

    parser = cmdline.build_parser()
    args = parser.parse_args(['get', '--multiThreaded', 'syn123'])

    assert_true(args.multiThreaded)

    args = parser.parse_args(['get', 'syn123'])
    assert_false(args.multiThreaded)


@patch('builtins.print')
def test_get_sts_token(mock_print):
    """Test getting an STS token."""
    folder_id = 'syn_1'
    permission = 'read_write'
    syn = Mock()

    expected_output = 'export foo=bar'
    syn.get_sts_storage_token.return_value = expected_output

    parser = cmdline.build_parser()
    args = parser.parse_args(['get-sts-token', folder_id, permission, '-o', 'shell'])
    cmdline.get_sts_token(args, syn)
    syn.get_sts_storage_token.assert_called_with(folder_id, permission, output_format='shell')

    mock_print.assert_called_once_with(expected_output)
