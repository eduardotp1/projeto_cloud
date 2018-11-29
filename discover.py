import os
import requests
import json
import sys
import boto3

with open('load.json') as f:
    info = json.load(f)


ACCESS_ID = info["ACCESS_ID"]
ACCESS_KEY = info["ACCESS_KEY"]

ec2 = boto3.client('ec2', region_name='us-east-1', aws_access_key_id=ACCESS_ID, aws_secret_access_key= ACCESS_KEY)


ip=''
existing_instances = ec2.describe_instances()
for i in range(len(existing_instances["Reservations"])):
    if ("Tags" in list(existing_instances["Reservations"][i]["Instances"][0].keys())):
        for tag in (existing_instances["Reservations"][i]["Instances"][0]["Tags"]):
            if(tag["Value"]=="tirta1"):
                status = (existing_instances["Reservations"][i]["Instances"][0]["State"]["Name"])
                if status == "running":
                    ip=existing_instances["Reservations"][i]["Instances"][0]["PublicIpAddress"]
print(ip)
