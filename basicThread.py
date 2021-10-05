import os
import re
import sys
import pdb
import time
import random
import argparse
from threading import Thread
from datetime import datetime
import verification_lib
import general_lib


## Run time arguments
parser = argparse.ArgumentParser(description='Parallel testing with "dd" command')
parser.add_argument('-thread_count','--thread_count',type=int, help='Number of threads count', required=True)
parser.add_argument('-bs','--bs', help='Bytesize of the file',required=True)
parser.add_argument('-src_cli_ip','--src_cli_ip', help='IP address of the source client', required=True)
parser.add_argument('-dst_cli_ip','--dst_cli_ip', help='IP address of the destination client', required=True)
args_out = parser.parse_args()
#log file creation
log_name = os.path.basename(__file__)
log_name = log_name +"_"+ str(datetime.now()) + ".log"
sys.stdout = open(os.getcwd()+"/Logs/"+log_name,"w")
err_log_name = os.path.basename(__file__)
err_log_name = err_log_name +"_"+ str(datetime.now()) + ".err"
sys.stderr = open(os.getcwd()+"/Logs/"+err_log_name,"w")

def verify_file_write_replication(rep_obj_src,rep_obj_dst,count,file_size,minusOne=False,plusOne=False,num_of_thread=1):
    # function call to get the ssh handle of source and destination
    rep_obj_src.login_to_host()
    rep_obj_dst.login_to_host()

    #Work around for 30 seconds delay in repilcation
    rep_obj_dst1 = general_lib.general_config('root',os.environ['script_s_key'],args_out.dst_cli_ip)
    rep_obj_dst1.login_to_host()


    # Object creation for the verification lib
    verify_obj = verification_lib.verification(rep_obj_src.hdl,rep_obj_dst.hdl)
    #print(count)
    for val in count:
       if minusOne:
          fname = "file_{0}m_urandom_{1}".format(int(val-1)*int(re.findall("\d",file_size)[0]),file_size)
          create_cmd = 'dd if=/dev/urandom of={0}/{1} bs={2} count={3}'.format(loc,fname,file_size,int(val-1))
       
       env.user = 'root'
       env.host_string = 'root@'+args_out.src_cli_ip
       env.password = os.environ['script_s_key']
       print("###########################################")
       print("Current time is {0}".format(datetime.now().strftime("%d.%b %Y %H:%M:%S")))
       print("###########################################")
       result = run(create_cmd)
       rep_obj_dst1.hdl.sendline("cat  /root/client1/{0} | tail -n 2".format(fname))
       rep_obj_dst1.hdl.expect_exact(["$","#"],300)
       #Checksum Verification function call
       print("###########################################")
       print("Current time is {0}".format(datetime.now().strftime("%d.%b %Y %H:%M:%S")))
       print("###########################################")
       out = verify_obj.cksum_compare(rep_obj_src.hdl,rep_obj_dst.hdl,lustre_mdt_loc,lustre_mdt_loc,fname)
       threading_out_list.append(out)

       ## FILE STAT Verification
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
          print("PASS :: Stats output is same for the file across the clients {0}".format(fname))
       else:
          print("FAIL :: Stats output is not same for the file across the clients {0}".format(fname))


       delete_cmd = 'rm -rf {0}/{1}'.format(loc,fname)
       rep_obj_src.hdl.sendline(delete_cmd)
       rep_obj_src.hdl.expect_exact(["#"],80)
    return threading_out_list

if __name__ == '__main__':

   env.user = 'root'
   env.host_string = 'root@10.1.1.1.'
   env.password = os.environ['script_s_key']

   # Object creation
   rep_obj_src = general_lib.general_config('root',os.environ['script_s_key'],args_out.src_cli_ip)
   rep_obj_dst = general_lib.general_config('root',os.environ['script_s_key'],args_out.dst_cli_ip)

   lustre_mdt_loc = '/root/client'
   threading_list = []
   threading_out_list = []
   obj_src_list = []
   obj_dest_list = []

   try :
      for i in range(args_out.thread_count):
         obj_src_list.append(general_lib.general_config('root',os.environ['script_s_key'],args_out.src_cli_ip))
         obj_dest_list.append(general_lib.general_config('root',os.environ['script_s_key'],args_out.dst_cli_ip))
      for src,dest in zip(obj_src_list,obj_dest_list):
         file_thread = Thread(target=verify_file_write_replication,args=(src,dest,[random.randint(100, 1000)],args_out.bs))
         threading_list.append(file_thread)
      for threads in threading_list:
         threads.start()
      for threads in threading_list:
         threads.join()
      #print(threading_out_list)
   except Exception as err:
      print("Exception seen :: {0} ".format(err))
