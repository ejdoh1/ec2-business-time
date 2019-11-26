import boto3

EC2 = boto3.client('ec2')
FILTER_ON = [{'Name': 'instance-state-name','Values': ['running']}]
FILTER_OFF = [{'Name': 'instance-state-name','Values': ['stopped']}]

def get_instances(filter):
    instance_ids = []
    paginator = EC2.get_paginator('describe_instances')
    pages = paginator.paginate(Filters=filter)
    for page in pages:
        reservations = page['Reservations']
        for r in reservations:
            instances = r['Instances']
            for i in instances:
                instance_ids.append(i['InstanceId'])
    return instance_ids

def on(event,context):
    i = get_instances(FILTER_OFF)
    print("turning on stopped instances:",i)
    r = EC2.start_instances(InstanceIds=i)
    print(r)

def off(event,context):
    i = get_instances(FILTER_ON)
    print("turning off running instances:",i)
    r = EC2.stop_instances(InstanceIds=i)
    print(r)
