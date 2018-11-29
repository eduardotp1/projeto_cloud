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
            if(tag["Value"]=="tirta"):
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
key_pair_info = ec2.import_key_pair(
    KeyName='teste',
    PublicKeyMaterial= chaver.read()
    )

response = ec2.describe_security_groups()
for key in response["SecurityGroups"]:
    if key["Description"]=="aps_tirta" and key["GroupName"]=="aps":
        response = ec2.delete_security_group(GroupName="aps")

ec2.create_security_group(
    Description='aps_tirta',
    GroupName='aps',
)

ec2.authorize_security_group_ingress(
    GroupName='aps',
    IpPermissions=[
        {'IpProtocol': 'tcp', 'FromPort': 5000, 'ToPort': 5000, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
        {'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
    ])

print("Creating Instance")
ec2_service.create_instances(ImageId='ami-0ac019f4fcb7cb7e6', MinCount=1, MaxCount=1,
    InstanceType='t2.micro',
    KeyName='teste',
    SecurityGroups=['aps'],
    UserData="""#!/bin/bash
            cd home/ubuntu/
            git clone https://github.com/eduardotp1/projeto_cloud.git
            sudo apt-get -y update
            sudo apt-get install -y python3-pip
            sudo pip3 install flask
            sudo pip3 install flask_restful
            sudo pip3 install boto3
            cd projeto_cloud/
            python3 load_balancer.py {0} {1} {2}
            """.format(info["ACCESS_ID"],info["ACCESS_KEY"],info["quant"]),
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Owner',
                    'Value': 'tirta1'
                },
            ]
        },
    ],
    )