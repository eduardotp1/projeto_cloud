import boto3
from time import sleep
import sys
import json

with open('load.json') as f:
    info = json.load(f)

ec2 = boto3.client('ec2')
s = boto3.Session(region_name="us-east-1")
ec2_service = s.resource('ec2')

response = ec2.describe_key_pairs()
chaver = open("teste.pub","r") 

existing_instances = ec2.describe_instances()
for i in range(len(existing_instances["Reservations"])):
    if ("Tags" in list(existing_instances["Reservations"][i]["Instances"][0].keys())):
        for tag in (existing_instances["Reservations"][i]["Instances"][0]["Tags"]):
            if(tag["Value"]=="tirta" or tag["Value"]=="tirta1"):
                ec2.terminate_instances(InstanceIds=[(existing_instances["Reservations"][i]["Instances"][0]["InstanceId"])])
                status=existing_instances["Reservations"][i]["Instances"][0]["State"]["Name"]
                while (status!="terminated"):
                    print(status)
                    existing_instances = ec2.describe_instances()
                    status=existing_instances["Reservations"][i]["Instances"][0]["State"]["Name"]
                    sleep(2) 
                    continue

for key in response["KeyPairs"]:
    if key["KeyName"]=="teste":
        ec2.delete_key_pair(KeyName='teste')

response = ec2.describe_security_groups()
for key in response["SecurityGroups"]:
    if key["Description"]=="aps_tirta" and key["GroupName"]=="aps":
        response = ec2.delete_security_group(GroupName="aps")
