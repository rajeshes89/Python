import boto.ec2.connection
import boto.ec2
import time
import sys
import pdb
import qa_env
import argparse
import os


def cleanup_existing_instances():
    #terminating existing connection
    reservations = c2c.get_all_instances()
    if reservations:
        instances_1 = [i for r in reservations for i in r.instances]
        for i in instances_1:
            if i.state == 'running':
                c2c.terminate_instances(instance_ids=[i.id])
                while i.update() != 'terminated':
                    time.sleep(5)
def launch_new_instances(ami,pem_key,inst_type='t2.micro',sec_key='default'):
    #Launching new instances
    for i in range(1):
        pdb.set_trace()
        c2c.run_instances(ami,key_name=pem_key,instance_type=inst_type,security_groups=[sec_key])
    time.sleep(60)

def get_public_private_ip():
    out1 = {}
    out2 = {}
    #Gather IP address of each instance
    reservations = c2c.get_all_instances()
    if reservations:
        instances_1 = [i for r in reservations for i in r.instances]
        for i in instances_1:
            if i.state == 'running':
                out1[i.id] = i.ip_address
                out2[i.id] = i.private_ip_address
    return out1,out2
if __name__ == '__main__':
    public_ip = {}
    private_ip = {}

    #connection object for the region
    c2c = boto.ec2.connect_to_region("us-east-1",aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"),aws_secret_access_key=os.environ.get("AWS_SECRET_KEY"))
    #cleanup_existing_instances()
    launch_new_instances('ami-02eac2c0129f6376b','kmesh-qa-key-coast1',inst_type='t2.micro',sec_key='default')
    #public_ip,private_ip = get_public_private_ip()
