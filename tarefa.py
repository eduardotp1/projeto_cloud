import os
import requests
import json
import sys
import boto3

ip=''
ec2 = boto3.client('ec2')
existing_instances = ec2.describe_instances()
for i in range(len(existing_instances["Reservations"])):
    if ("Tags" in list(existing_instances["Reservations"][i]["Instances"][0].keys())):
        for tag in (existing_instances["Reservations"][i]["Instances"][0]["Tags"]):
            if(tag["Value"]=="tirta1"):
                status = (existing_instances["Reservations"][i]["Instances"][0]["State"]["Name"])
                if status == "running":
                    ip=existing_instances["Reservations"][i]["Instances"][0]["PublicIpAddress"]

print(ip)

numeros = json.dumps({"arg1":sys.argv[1],"arg2":sys.argv[2]})

headers = {'content-type': 'application/json'}
req = requests.get('http://'+ip+':5000/Multiplicador/',data=numeros,headers=headers )

print (req.text)