import unittest
import central_system
from POD import POD
import sys
import filecmp
import time
from multiprocessing import Process

central_create = "python central_system.py"

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


class TestFramework(unittest.TestCase):
    """Test cases for the protocol"""

    @classmethod
    def setUpClass(self):
        """Prepare for testing"""
        # default netem rule (does nothing)
        print("----------------setup--------------------------")
        # launch localhost server
        self.server_process = Process(target=central_system.main)
        self.server_process.start()
        time.sleep(0.1)

    @classmethod
    def tearDownClass(self):
        """Clean up after testing"""
        # clean the environment
        # close server
        
        self.server_process.kill()
        # already closed
        print("-------------------teardown-----------------------")

    def test_pod_id(self):
        # create classes
        pod = POD('xd')
        
        # check if the ID is right
        self.assertEqual('asdsahudiah', pod.ID)
        
    def test_bus_stop(self):
        # create classes
        station1 = Station('Centraal Station', 'ad')
        pod = POD('xd')
        
        # ask for a POD
        station1.callshuttle()
        
        
        self.assertEqual('asdsahudiah', pod.ID)
        
    

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
