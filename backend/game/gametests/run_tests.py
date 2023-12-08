# test runner
import os
import sys
import time
CURRENT_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(CURRENT_DIR)
G_PARENT_DIR = os.path.dirname(PARENT_DIR)
sys.path.append(os.path.dirname(G_PARENT_DIR))

import pytest

# Get all test module filenames
test_modules = [f for f in os.listdir() if f.startswith("test")]

# Create argument list 
args = ["-v"]
args.extend(test_modules)

# Run pytest over all test modules
ret = pytest.main(args)

# Return exit code back to calling process  
exit(ret)