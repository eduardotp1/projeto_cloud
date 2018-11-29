import boto3
from time import sleep
from flask import Flask, redirect, url_for, request
from flask_restful import Api, Resource
import json
import random
from threading import Thread,Timer
import time
import requests
import sys

if len(sys.argv)==4:
    quant=sys.argv[3]
else:
    quant=3

ACCESS_ID = sys.argv[1]
ACCESS_KEY = sys.argv[2]

app = Flask(__name__)

ec2 = boto3.client('ec2', region_name='us-east-1', aws_access_key_id=ACCESS_ID, aws_secret_access_key= ACCESS_KEY)
ec2_service = boto3.resource('ec2', region_name='us-east-1', aws_access_key_id=ACCESS_ID, aws_secret_access_key= ACCESS_KEY)

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
                    python3 app.py
                    """,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Owner',
                            'Value': 'tirta'
                        },
                    ]
                },
            ],
            )
time.sleep(120)
existing_instances = ec2.describe_instances()
pub_ip={}
for i in (existing_instances["Reservations"]):
    if ("Tags" in list(i["Instances"][0].keys())):
        for tag in (i["Instances"][0]["Tags"]):
            if(tag["Value"]=="tirta"):
                status = i["Instances"][0]["State"]["Name"]
                if status == "running":
                    pub_ip[(i["Instances"][0]["InstanceId"])]= i["Instances"][0]["PublicIpAddress"]
print("As publics IP que estao rodando sao: ", pub_ip)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    global pub_ip
    ip = random.choice(list(pub_ip.values()))
    return redirect("http://" + ip + ":5000/" + path,code=307)



#https://www.saltycrane.com/blog/2008/09/simplistic-python-thread-example/
def timeout():
    print("Deu ruim... timeout")
    global id_atual
    global pub_ip
    global quant
    print("a id que falhou eh",id_atual)
    existing_instances = ec2.describe_instances()
    ec2.terminate_instances(InstanceIds=[id_atual])
    
    

    
    existing_instances = ec2.describe_instances()
    for i in range(len(existing_instances["Reservations"])):
        for tag in (existing_instances["Reservations"][i]["Instances"]):
            if(tag["InstanceId"]==id_atual):
                status=existing_instances["Reservations"][i]["Instances"][0]["State"]["Name"]
                while (status!="terminated"):
                    existing_instances = ec2.describe_instances()
                    status=existing_instances["Reservations"][i]["Instances"][0]["State"]["Name"]
                    time.sleep(8)
                    continue
    pub_ip={}
    existing_instances = ec2.describe_instances()
    for i in (existing_instances["Reservations"]):
        if ("Tags" in list(i["Instances"][0].keys())):
            for tag in (i["Instances"][0]["Tags"]):
                if(tag["Value"]=="tirta"):
                    status = i["Instances"][0]["State"]["Name"]
                    if status == "running":
                        pub_ip[(i["Instances"][0]["InstanceId"])]= i["Instances"][0]["PublicIpAddress"]


    if (len(list(pub_ip.values())))>int(quant):
        existing_instances = ec2.describe_instances()
        id_extra=random.choice(list(pub_ip.keys()))
        ec2.terminate_instances(InstanceIds=[id_extra])
        existing_instances = ec2.describe_instances()
        for i in range(len(existing_instances["Reservations"])):
            for tag in (existing_instances["Reservations"][i]["Instances"]):
                if(tag["InstanceId"]==id_atual):
                    status=existing_instances["Reservations"][i]["Instances"][0]["State"]["Name"]
                    while (status!="terminated"):
                        existing_instances = ec2.describe_instances()
                        status=existing_instances["Reservations"][i]["Instances"][0]["State"]["Name"]
                        time.sleep(8)
                        continue



    while(len(list(pub_ip.values()))<int(quant)):
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
                    python3 app.py
                    """,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Owner',
                            'Value': 'tirta'
                        },
                    ]
                },
            ],
            )
        time.sleep(120)
        pub_ip={}

        existing_instances = ec2.describe_instances()
        for i in (existing_instances["Reservations"]):
            if ("Tags" in list(i["Instances"][0].keys())):
                for tag in (i["Instances"][0]["Tags"]):
                    if(tag["Value"]=="tirta"):
                        status = i["Instances"][0]["State"]["Name"]
                        if status == "running":
                            pub_ip[(i["Instances"][0]["InstanceId"])]= i["Instances"][0]["PublicIpAddress"]
    

    existing_instances = ec2.describe_instances()
    for i in (existing_instances["Reservations"]):
        if ("Tags" in list(i["Instances"][0].keys())):
            for tag in (i["Instances"][0]["Tags"]):
                if(tag["Value"]=="tirta"):
                    status = i["Instances"][0]["State"]["Name"]
                    if status == "running":
                        pub_ip[(i["Instances"][0]["InstanceId"])]= i["Instances"][0]["PublicIpAddress"]

    health()

if (len(list(pub_ip.values()))!=0):
    id_atual = list(pub_ip.values())[0]
def health():
    global pub_ip
    global id_atual
    global quant
    while(True):
        if (len(list(pub_ip.keys()))<int(quant)):
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
                        python3 app.py
                        """,
                TagSpecifications=[
                    {
                        'ResourceType': 'instance',
                        'Tags': [
                            {
                                'Key': 'Owner',
                                'Value': 'tirta'
                            },
                        ]
                    },
                ],
                )
            time.sleep(120)

        elif (len(list(pub_ip.values()))>int(quant)):
            existing_instances = ec2.describe_instances()
            id_extra=random.choice(list(pub_ip.keys()))
            ec2.terminate_instances(InstanceIds=[id_extra])
            existing_instances = ec2.describe_instances()
            for i in range(len(existing_instances["Reservations"])):
                for tag in (existing_instances["Reservations"][i]["Instances"]):
                    if(tag["InstanceId"]==id_atual):
                        status=existing_instances["Reservations"][i]["Instances"][0]["State"]["Name"]
                        while (status!="terminated"):
                            existing_instances = ec2.describe_instances()
                            status=existing_instances["Reservations"][i]["Instances"][0]["State"]["Name"]
                            time.sleep(8)
                            continue


        pub_ip={}
        existing_instances = ec2.describe_instances()
        for i in (existing_instances["Reservations"]):
            if ("Tags" in list(i["Instances"][0].keys())):
                for tag in (i["Instances"][0]["Tags"]):
                    if(tag["Value"]=="tirta"):
                        status = i["Instances"][0]["State"]["Name"]
                        if status == "running":
                            pub_ip[(i["Instances"][0]["InstanceId"])]= i["Instances"][0]["PublicIpAddress"]


        for key, values in pub_ip.items():
            id_atual=key
            t = Timer(50.0,timeout)
            t.start()
            try:
                r=requests.get('http://' + values + ':5000/healthcheck')
            except:
                pass

            t.cancel()
        time.sleep(2)

t = Thread(target=health)
t.start()

app.run(host='0.0.0.0', port=5000)