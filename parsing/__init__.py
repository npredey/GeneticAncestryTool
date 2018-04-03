import os
import sys
# https://stackoverflow.com/questions/448271/what-is-init-py-for
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR)

sys.path.append(os.path.dirname(os.getcwd()))
from wrapper.wrapper_util import call_plink