import logging
import argparse
import sys

parser = argparse.ArgumentParser(description='Basic Testing')
parser.add_argument('-f','--conf_file', help='Script Config file', required=True)
parser.add_argument('-t','--tag',help='tag name for identity',required=True)
args_out = parser.parse_args()
script_config = args_out.conf_file

exec(open(script_config).read()) #execfile equivalent 
log_file_name = "/tmp/logs/"+sys.argv[0].strip(".py").split("/")[-1]+time.strftime("_%Y-%m-%d_%H%M%S")+"-"+args_out.tag+".log"
logging.basicConfig(filename = log_file_name,level=logging.DEBUG,format='%(asctime)s %(levelname)-8s %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
