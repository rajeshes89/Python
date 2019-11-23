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

def verify_file_order_with_replication(rep_obj_src,rep_obj_dst):
    # Object creation to get ssh handle for src and dest
    rep_obj_src.login_to_host()
    rep_obj_src1.login_to_host()
    rep_obj_dst.login_to_host()
    rep_obj_dst1.login_to_host()
    # Object creation for verification library
    verify_obj = verification_lib.verification(rep_obj_src.hdl,rep_obj_dst.hdl)
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
       filename_list.append(fname)
       rep_obj_src.hdl.sendline("touch {0}/{1}".format(lustre_mdt_loc,fname))
       rep_obj_src.hdl.expect_exact(["$","#"],80)
       rep_obj_src.hdl.sendline("echo {2} > {0}/{1}".format(lustre_mdt_loc,fname,random_data))
       rep_obj_src.hdl.expect_exact(["$","#"],80)
       time.sleep(1)
    ## CKSUM Verification
    for fname in filename_list:
       # cksum comparison function call for each file
       print("###########################################")
       print("Current time is {0}".format(datetime.now().strftime("%d.%b %Y %H:%M:%S")))
       print("###########################################")
       verify_obj.cksum_compare(rep_obj_src.hdl,rep_obj_dst.hdl,lustre_mdt_loc,lustre_mdt_loc,fname)

    ## FILE ORDER Verification
    rep_obj_src.hdl.sendline("ls -lrt {0} | awk '{{print $9}}'".format(lustre_mdt_loc))
    rep_obj_src.hdl.expect_exact(["#"],300)
    fname_list = re.findall("\w{10}",rep_obj_src.hdl.before)
    rep_obj_dst.hdl.sendline("ls -lrt {0} | awk '{{print $9}}'".format(lustre_mdt_loc))
    rep_obj_dst.hdl.expect_exact(["#"],300)
    fname_list_dst = re.findall("\w{10}",rep_obj_dst.hdl.before)
    if fname_list == fname_list_dst :
       print("PASS :: File ordering is same across source and destination client \n")
    else:
       print("FAIL :: File ordering is different across source and destination client\n")

    ## FILE STAT Verification
    for fname in fname_list:
       fname = fname.strip("\r")
       print("###########################################")
       print("Current time is {0}".format(datetime.now().strftime("%d.%b %Y %H:%M:%S")))
       print("###########################################")
       src_out = verify_obj.stat_out_verification(rep_obj_src.hdl,lustre_mdt_loc,fname)
       print("###########################################")
       print("Current time is {0}".format(datetime.now().strftime("%d.%b %Y %H:%M:%S")))
       print("###########################################")
       dest_out = verify_obj.stat_out_verification(rep_obj_dst.hdl,lustre_mdt_loc,fname)
       if src_out != False and dest_out != False \
          and src_out == dest_out:
          print("PASS :: Stats output is same for the file across the clients for file {0}\n".format(fname))
       else:
          print("FAIL :: Stats output is not same for the file across the clients for file {0}\n".format(fname))


if __name__ == '__main__':

   filename_list = []
   lustre_mdt_loc = '/root/client/dir1/testOne'
   global ls_out_src
   global ls_out_dst
   # Object creation for creating general lib
   rep_obj_src = general_lib.general_config('root',os.environ['script_s_key'],args_out.src_cli_ip)
   rep_obj_dst = general_lib.general_config('root',os.environ['script_s_key'],args_out.dst_cli_ip)
   rep_obj_src1 = general_lib.general_config('root',os.environ['script_s_key'],args_out.src_cli_ip)
   rep_obj_dst1 = general_lib.general_config('root',os.environ['script_s_key'],args_out.dst_cli_ip)

   try :
      verify_file_order_with_replication(rep_obj_src,rep_obj_dst)
   except Exception as err:
      print("Exception seen :: {0} ".format(err))
