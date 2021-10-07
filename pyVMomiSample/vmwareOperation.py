import os
import re
import argparse
from threading import Thread
import logging
import pdb
import sys
import atexit
from pyVim import connect
from pyVmomi import vmodl
from pyVmomi import vim
import time
from fabric.api import run, sudo, env,put,hide,settings
from fabric.state import output

parser = argparse.ArgumentParser()
parser.add_argument('-f','--conf_file', help='Script Config file', required=True)
parser.add_argument('-s','--suite_file',nargs='+', help='Suite files seperated by space ', required=True)
parser.add_argument('-d','--deleteVM', help='VM deletion confirmation',default=False)
args_out = parser.parse_args()
suite_file = args_out.suite_file
script_config = args_out.conf_file
vm_del = args_out.deleteVM
execfile(script_config)

# create logger & handler
os.system("rm -rf {0}".format(log_name))
logging.basicConfig(filename=log_name,level='INFO', format="%(asctime)s: %(levelname)s: %(message)s", datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger("ClientVMLaunch")
logger.setLevel(logging.INFO)
logging.getLogger("paramiko").setLevel(logging.WARNING)

def fabric_bootstrap(user=None, ipv4=None, deployment="aws", keyfile=None, passwd=None):
    """ create the ssh connection to ec2 instances with credentials provided """

    env.user = user
    env.host_string = "%s@%s" %(user, ipv4)
    env.sudo_prefix = "sudo"
    env.warn_only = True
    if deployment == "aws":
        env.key_filename = keyfile
    elif deployment == "private":
        env.password = passwd
        env.no_agent = True
        env.abort_on_prompts = True

#Create OVF based on the given template
def create_ovf(template,ovf_dir):
    #ovftool  vi://administrator@kabcd.io:abcd124@10.40.16.149/dc1.abcd.io/vm/Lustre_test test.ovf
    cmd = "ovftool vi://{0}:{1}@{2}/{3}/vm/{4} {5}".format(user,pwd,vcenter_ip,datacenter,template,ovf_dir)
    logger.info("Running the cmd {0}".format(cmd))
    logger.info(os.system(cmd))

#OVF to vm launch
def launch_ovf(inst_name,template,ovf_dir):
    ovf_path = ovf_dir+"/"+template+"/"+template+".ovf"
    #cmd = "ovftool -n='basic_test' -ds='NVM' test.ovf vi://administrator@test.io:test@10.10.10.10/?ip=10.10.10.11"
    cmd = "ovftool --powerOn -n={0} -ds={1} {2} vi://{3}:{4}@{5}/?ip={6}".format(inst_name,data_store,ovf_path,user,pwd,vcenter_ip,host_ip)
    logger.info("Running the cmd {0}".format(cmd))
    logger.info(os.system(cmd))

#Get the ip's of the VM
def get_node_details(ip,user,pwd,vm_list):
    node_ips = []
    service_instance = connect.SmartConnectNoSSL(host=ip,user=user,pwd=pwd)
    content = service_instance.RetrieveContent()
    container = content.rootFolder
    viewType = [vim.VirtualMachine]
    containerView = content.viewManager.CreateContainerView(container, viewType, True)
    children = containerView.view
    logger.info("Getting the ip list of the vm list {0}".format(vm_list))
    for name in vm_list:
        for val in range(len(children)):
            if name == children[val].name:
                node_ips.append(children[val].summary.guest.ipAddress)
                logger.info("Ip address of the vm {0} is {1}".format(name,children[val].summary.guest.ipAddress))
                break;

    return node_ips

def launch_vm_get_details(vm_template,ovf_dir,inst_name,vm_count):
    global vm_name_list
    threading_list = []
    vm_list = []
    create_ovf(vm_template,ovf_dir)
    vm_name_list = [inst_name] * vm_count
    for i,j in zip(range(vm_count),vm_name_list):
       file_thread = Thread(target=launch_ovf,args=(j+str(i),vm_template,ovf_dir))
       vm_list.append(j+str(i))
       threading_list.append(file_thread)
    for threads in threading_list:
       threads.start()
    for threads in threading_list:
       threads.join()
    logger.info("Waiting to get the ip address..")
    print("Waiting to get the ip address..")
    time.sleep(120)
    ip_list = get_node_details(vcenter_ip,user,pwd,vm_list)
    return ip_list,vm_list


def main():
    client_ips,client_vms = launch_vm_get_details(c_template,c_ovf_dir,c_inst_name,c_vm_count)
    logger.info("The Client VM list is {0} and their ip's are {1}".format(client_vms,client_ips))
    server_ips,server_vms = launch_vm_get_details(s_template,s_ovf_dir,s_inst_name,s_vm_count)
    logger.info("The Server VM list is {0} and their ip's are {1}".format(server_vms,server_ips))
    for vm in server_vms:
        for i in range(3):
            os.system("python vm_utils/add_disk_vm.py -s {0} -u {1} -p {2} --disk-size {3} -v {4}".format(vcenter_ip,user,pwd,25,vm))
    return client_ips,server_ips
#if __name__ == '__main__':
#    try :
#        main()
#    except Exception as err:
#        logger.info("Exception seen :: {0}".format(err))
