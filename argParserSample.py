import os
import re
import sys
sys.path.append("/root/kmesh-dataplane-test/fileSystem/automation/featureTesting/kmeshFilesystemTests/tests")
import pdb
import time
import random
import string
import argparse
from datetime import datetime
sys.path.append("/automation/lib")
import general_lib
import verification_lib

## Run time arguments
parser = argparse.ArgumentParser(description='file creation and order verification using ls -lrt')
parser.add_argument('-files_count','--files_count',type=int, help='Number of files count', required=True)
parser.add_argument('-src_cli_ip','--src_cli_ip', help='IP address of the source client', required=True)
parser.add_argument('-dst_cli_ip','--dst_cli_ip', help='IP address of the destination client', required=True)
args_out = parser.parse_args()

#log file creation
#os.system("mkdir {0}/Logs".format(os.getcwd()))
log_name = os.path.basename(__file__)
log_name = log_name +"_"+ str(datetime.now()) + ".log"
sys.stdout = open(os.getcwd()+"/Logs/"+log_name,"w")
err_log_name = os.path.basename(__file__)
err_log_name = err_log_name +"_"+ str(datetime.now()) + ".err"
sys.stderr = open(os.getcwd()+"/Logs/"+err_log_name,"w")

def verify_file(src,dst):
    # Removing the existing directory and creating newly in src and dest
    for obj in [rep_obj_src,rep_obj_dst]:
       obj.hdl.sendline("rm -rf {0}".format(lustre_mdt_loc))
       obj.hdl.expect_exact(["$","#"],30)
       obj.hdl.sendline("mkdir {0}".format(lustre_mdt_loc))
       obj.hdl.expect_exact(["$","#"],30)
    #Random string name creation to create a file using 'touch' and echo sample string
    for i in range(args_out.files_count): #10 indicates number of files
       fname = ''.join([random.choice(string.ascii_lowercase) for i in range(10)]) #10 indicates string length
       random_data = ''.join([random.choice(string.ascii_lowercase) for i in range(5)])
    
