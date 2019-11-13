#! /usr/bin/python
import requests
import json
import logging
import pdb
import re
import argparse
​
# create logger & handler
logging.basicConfig(filename='/tmp/rest_api.log',level='INFO', format="%(asctime)s: %(levelname)s: %(message)s", datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger("RestApiTest")
logger.setLevel(logging.INFO)
logging.getLogger("paramiko").setLevel(logging.WARNING)
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config_file", required=True, help="The config file to be used")
args_out = parser.parse_args()
execfile(args_out.config_file)
​
def login_api(url):
    payload = {"username":"admin@kmesh.io","password":{"account_id":"111122223333","password":"ssaf"}}
    r = requests.post(url, data=json.dumps(payload),headers={"content-type":"application/json"})
    print(r.status_code,r.text)
    return json.loads(r.text)
​
def aws_global_setting(src_url,token,payload):
    r = requests.post(src_url, data=json.dumps(payload),headers={"content-type":"application/json","Authorization":"JWT " + token})
    print(r.status_code,r.text)
    return r.status_code
​
def create_profile(src_url,token,payload):
    r = requests.post(src_url, data=json.dumps(payload),headers={"content-type":"application/json","Authorization":"JWT " + token})
    print(r.status_code,r.text)
    return r.status_code
​
def create_node(url,cloud_type,token,payload):
    src_url = url + '/api/{0}profile'.format(cloud_type)
    out = requests.get(src_url,headers={"content-type":"application/json","Authorization":"JWT " + token})
    if re.search("aws",cloud_type):
        payload["profile_id"] = json.loads(out.text)[0]['id']
    elif re.search("vsphere",cloud_type):
        payload['vsphere_profile_id'] = json.loads(out.text)[0]['id']
    elif re.search("azure",cloud_type):
        payload['azure_profile_id'] = json.loads(out.text)[0]['id']
    src_url = url + '/api/filesystem'
    r = requests.post(src_url, data=json.dumps(payload),headers={"content-type":"application/json","Authorization":"JWT " + token})
    print(r.status_code,r.text)
    return r.status_code
​
def get_id(url,token,keyname,node_name):
    out = requests.get(url,headers={"content-type":"application/json","Authorization":"JWT " + token})
    for node_list in json.loads(out.text):
        if node_list[keyname] == node_name:
            return node_list['id']
            break
def dataflow_create(url,url2,token,payload,node1,node2,df_name):
    payload['source_node_id'] = get_id(url,token,'node_name',node1)
    payload['dest_node_id'] = get_id(url,token,'node_name',node2)
    payload['dataflow_name'] = df_name
    payload['data_path'] = df_name
    r = requests.post(url2, data=json.dumps(payload),headers={"content-type":"application/json","Authorization":"JWT " + token})
    return r.status_code
​
def dataflow_launch(get_url,launch_url,token,payload=None,df_name=None):
    df_id = get_id(get_url,token,'dataflow_name',df_name)
    payload["dataflow_id"] = [df_id]
    r = requests.post(launch_url, data=json.dumps(payload),headers={"content-type":"application/json","Authorization":"JWT " + token})
    return r.status_code
​
if __name__ == '__main__':
​
    token = login_api(auth_url)['access_token']
    aws_global = aws_global_setting(aws_global_settings_url,token,aws_global_payload)
    out = create_profile(aws_profile_url,token,aws_profile_payload)
    out = create_profile(vsphere_profile_url,token,vsphere_profile_payload)
    out = create_profile(azure_profile_url,token,azure_profile_payload)
    #node_out = create_node(url,'aws',token,aws_node_payload)
    node_out = create_node(url,'vsphere',token,vmware_node_payload)
    node_out = create_node(url,'vsphere',token,vmware_node_payload2)
    #node_out = create_node(url,'azure',token,azure_node_payload)
    #dataflow_out = dataflow_create(filesystem_url,dataflow_url,token,dataflow_payload,"vmware-node1","aws-node1","VM-AWS")
    dataflow_out = dataflow_create(filesystem_url,dataflow_url,token,dataflow_payload,"rajesh-node1","rajesh-node2","VM-VM-DF")
    dataflow_launch_out = dataflow_launch(dataflow_url,dataflow_launch_url,token,dataflow_deploy_payload,df_name='VM-VM-DF')
