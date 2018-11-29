import os
import requests
import json
import sys
import boto3



arg1=sys.argv[1]
arg2=sys.argv[2]

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


req = requests.get('http://'+ip+':5000/Multiplicador/{0}/{1}'.format(int(arg1),int(arg2)))

print (req.text)