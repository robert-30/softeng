import unittest
import central_system

import sys
import filecmp
from multiprocessing import Process

timeout = 100
winsize = 100
intf = "lo"
netem_add = "sudo tc qdisc add dev {} root netem".format(intf)
netem_change = "sudo tc qdisc change dev {} root netem {}".format(intf, "{}")
netem_del = "sudo tc qdisc del dev {} root netem".format(intf)


"""run command and retrieve output"""


def run_command_with_output(command, input=None, cwd=None, shell=True):
    import subprocess
    try:
        process = subprocess.Popen(command, cwd=cwd, shell=shell, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    except Exception as inst:
        print("problem running command : \n   ", str(command))

    [stdoutdata, stderrdata] = process.communicate(
        input)  # no pipes set for stdin/stdout/stdout streams so does effectively only just wait for process ends  (same as process.wait()

    if process.returncode:
        print(stderrdata)
        print("problem running command : \n   ", str(command), " ", process.returncode)

    return stdoutdata


"""run command with no output piping"""


def run_command(command, cwd=None, shell=True):
    import subprocess
    process = None
    try:
        process = subprocess.Popen(command, shell=shell, cwd=cwd)
        print(str(process))
    except Exception as inst:
        print("1. problem running command : \n   ", str(command), "\n problem : ", str(inst))

    process.communicate()  # wait for the process to end

    if process.returncode:
        print("2. problem running command : \n   ", str(command), " ", process.returncode)


class TestbTCPFramework(unittest.TestCase):
    """Test cases for bTCP"""

    def setUp(self):
        """Prepare for testing"""
        # default netem rule (does nothing)
        print("------------------------------------------")
        run_command(netem_add)
        # launch localhost server
        self.server_process = Process(target=server_app.main, args=(winsize, timeout, output_file))
        self.server_process.start()

    def tearDown(self):
        """Clean up after testing"""
        # clean the environment
        run_command(netem_del)
        # close server
        # already closed
        print("------------------------------------------")

    def test_ideal_network(self):
        """reliability over an ideal framework"""
        # setup environment (nothing to set)

        # launch localhost client connecting to server
        print()
        print("Case 'test_ideal_network':")
        client_process = Process(target=client_app.main, args=(winsize, timeout, input_file))
        # client sends content to server
        client_process.start()
        # server receives content from client
        client_process.join()
        self.server_process.join()
        # content received by server matches the content sent by client
        if filecmp.cmp(input_file, output_file):
            self.assertTrue(True)
            print("Test ended successfully!")
            print()
        else:
            self.assertTrue(False)
            print("Something went wrong!")
            print()

if __name__ == "__main__":
    # Parse command line arguments
    import argparse

    parser = argparse.ArgumentParser(description="bTCP tests")
    parser.add_argument("-w", "--window", help="Define bTCP client window size used", type=int, default=50)
    parser.add_argument("-t", "--timeout", help="Define the client/server timeout value used (ms)", type=int, default=700)
    parser.add_argument("-i", "--input", help="File to send", default="input.file")
    parser.add_argument("-o", "--output", help="Where to store the file", default="output.file")
    args, extra = parser.parse_known_args()

    timeout = args.timeout
    winsize = args.window
    input_file = args.input
    output_file = args.output

    # Pass the extra arguments to unittest
    sys.argv[1:] = extra

    # Start test suite
    unittest.main()