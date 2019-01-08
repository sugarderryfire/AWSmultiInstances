# -*- coding: utf-8 -*-

# Boto 3
import boto3
import time
import sys
import paramiko
import base64
import os
import random
import subprocess
import threading



#hostIP="54.152.202.91"
runningInstances=[]
regionList=["us-east-1","us-east-2","us-west-1","us-west-2","eu-west-2","ap-southeast-2","ap-northeast-1","eu-central-1"]
imageList=["ami-0ac019f4fcb7cb7e6","ami-0f65671a86f061fcd","ami-063aa838bd7631e0b","ami-0bbe6b35405ecebdb","ami-0b0a60c0a2bd40612","ami-07a3bd4944eb120a0","ami-07ad4b1c3af1ea214","ami-0bdf93799014acdc4"]
chosenImage=""
currentRegionName=""
currentImage=""
minInstances=2
maxInstances=4


def config_instances():
    outfile = open('ec2keyInstance4.pem','w')
    key_pair = ec2.create_key_pair(KeyName='ec2keyInstance4')
    KeyPairOut = str(key_pair.key_material)
    outfile.write(KeyPairOut)


def create_instances():
    #create instances.
    global currentImage
    ec2_instances = ec2.create_instances(ImageId=currentImage,MinCount=1,MaxCount=1,KeyName="ec2keyInstance4",InstanceType='t2.micro')
    time.sleep(10)
    return ec2_instances


def create_Multiinstances(instancesRandNumber):
    #create instances.
    global currentImage,minInstances,maxInstances
    ec2_instances = ec2.create_instances(ImageId=currentImage,MinCount=minInstances,MaxCount=instancesRandNumber,KeyName="ec2keyInstance4",InstanceType='t2.micro')
    time.sleep(10)
    return ec2_instances


def execute_command(hostIP):
    key = paramiko.RSAKey.from_private_key_file('ec2keyInstance4.pem')
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Connect/ssh to an instance
    try:
        # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2
        client.connect(hostname=hostIP, username="ubuntu", pkey=key)
        execute(client,'wget https://github.com/sugarderryfire/AutomAmazonFIles/blob/master/geckodriver?raw=true')
	execute(client,'mv geckodriver\?raw\=true geckodriver')
        execute(client,'wget https://raw.githubusercontent.com/sugarderryfire/AutomAmazonFIles/master/Automain.py')
        execute(client,'sudo apt -y install python')
        execute(client,'sudo apt update')
        execute(client,'sudo apt -y install python-pip')
	execute(client,'sudo pip install selenium')
	execute(client,'sudo pip install xlrd')
	execute(client,'sudo pip install pandas')
	execute(client,'sudo pip install openpyxl')
	execute(client,'sudo pip install stem')
	execute(client,'sudo pip install splinter')
	execute(client,'sudo apt -y install xvfb')
	#execute(client,'export DISPLAY=:99')
        # close the client connection once the job is done
   	client.close()
    except Exception, e:
        print e


def execute_command2(hostIP):
    key = paramiko.RSAKey.from_private_key_file('ec2keyInstance4.pem')
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Connect/ssh to an instance
    try:
	time.sleep(5)
	print 'second stage'
        # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2
        client.connect(hostname=hostIP, username="ubuntu", pkey=key)
	execute(client,'sudo cp geckodriver /usr/local/bin/geckodriver')
	execute(client,'sudo chmod +x /usr/local/bin/geckodriver')
	execute(client,'sudo apt-get -y install firefox')
        # close the client connection once the job is done
   	client.close()
    except Exception, e:
        print e



def execute_command3(hostIP):
    mandatoryCommand="cat scr.sh | ssh -o StrictHostKeyChecking=no -i ec2keyInstance4.pem ubuntu@"
    mandatoryCommand=mandatoryCommand+hostIP
#    mandatoryCommand=mandatoryCommand+ " |"
    #mandatoryCommand=mandatoryCommand + " && exit"
    key = paramiko.RSAKey.from_private_key_file('ec2keyInstance4.pem')
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Connect/ssh to an instance
    try:
	time.sleep(5)
	print 'third stage'
        # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2
        client.connect(hostname=hostIP, username="ubuntu", pkey=key)
	execute(client,'sudo apt -y install xvfb')
#	execute(client,comm1)
        #execute(client,comm2)
	mandatoryCommand=mandatoryCommand+" &"
	os.system(mandatoryCommand)
	#execute(client,mandatoryCommand)
	#returned_output = subprocess.check_output(mandatoryCommand)	
	print 'test1v'
	#execute(client,'python Automain.py blockchain block.chain.technology')
        # close the client connection once the job is done
   	client.close()
    except Exception, e:
        print e




def execute(client,command):
    try:
        print 'running remote command'
        # Execute a command(cmd) after connecting/ssh to an instance
        stdin, stdout, stderr = client.exec_command(command)
        print stdout.read()
    except Exception, e:
        print e
	




def terminate_instances():
    print 'terminate'
    #terminate instances in ec2_instances arrן
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for instance in instances:
	instance.terminate()
	print instance.public_ip_address



def get_instances():
    # Boto 3
    # Use the filter() method of the instances collection to retrieve
    # all running EC2 instances.
    instancesList=[]
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for instance in instances:
	instancesList.append(instance.public_ip_address)
	print(instance.id, instance.instance_type,instance.public_ip_address)
    return instancesList


def get_first_instance():
    # Boto 3
    # Use the filter() method of the instances collection to retrieve
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for instance in instances:
	return instance.public_ip_address

   

def commit_instanceFromRegion():
    # Boto 3
    # Use the filter() method of the instances collection to retrieve
    #time.sleep(100)
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for instance in instances:
	hostIP=instance.public_ip_address
	commit_all(hostIP)



def get_currentRegion():
    global chosenImage
    listLen=len(regionList)
    chosenIndex=random.randint(0,listLen-1)
    chosenImage=imageList[chosenIndex]
    return regionList[chosenIndex]


def get_random(min1,max1):
    chosenNumber=random.randint(min1-1,max1-1)
    return chosenNumber


def commit_all(hostIP):
    mandatoryCommand="cat scr.sh | ssh -o StrictHostKeyChecking=no -i ec2keyInstance4.pem ubuntu@"
    mandatoryCommand=mandatoryCommand+hostIP
    key = paramiko.RSAKey.from_private_key_file('ec2keyInstance4.pem')
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Connect/ssh to an instance
    try:
        # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2
        client.connect(hostname=hostIP, username="ubuntu", pkey=key)
        execute(client,'wget https://github.com/sugarderryfire/AutomAmazonFIles/blob/master/geckodriver?raw=true')
	execute(client,'mv geckodriver\?raw\=true geckodriver')
        execute(client,'wget https://raw.githubusercontent.com/sugarderryfire/AutomAmazonFIles/master/Automain.py')
        execute(client,'sudo apt -y install python')
        execute(client,'sudo apt update')
        execute(client,'sudo apt -y install python-pip')
	execute(client,'sudo pip install selenium')
	execute(client,'sudo pip install xlrd')
	execute(client,'sudo pip install pandas')
	execute(client,'sudo pip install openpyxl')
	execute(client,'sudo pip install stem')
	execute(client,'sudo pip install splinter')
	execute(client,'sudo apt -y install xvfb')
	time.sleep(5)
	print 'second stage'
        # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2
	execute(client,'sudo cp geckodriver /usr/local/bin/geckodriver')
	execute(client,'sudo chmod +x /usr/local/bin/geckodriver')
	execute(client,'sudo apt-get -y install firefox')
	time.sleep(5)
	print 'third stage'
        # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2
        client.connect(hostname=hostIP, username="ubuntu", pkey=key)
	execute(client,'sudo apt -y install xvfb')
	mandatoryCommand=mandatoryCommand+" &"
	os.system(mandatoryCommand)
        # close the client connection once the job is done
   	client.close()
    except Exception, e:
        print e



#need to be cinfigured to the current region with key pair
def delete_key_pair():
    #ec2 = boto3.client('ec2',region_name="us-east-1")
    response = ec3.delete_key_pair(KeyName='ec2keyInstance4')




# delete all keys in all regions.
def delete_all_keys():
    counter=0
    listLength=len(regionList)
    while(True):
        currentRegionName=regionList[counter]
        ec3 = boto3.client('ec2',region_name=currentRegionName)
	response = ec2.delete_key_pair(KeyName='ec2keyInstance4')
	counter=counter+1
	if(counter==listLength-1):
	    counter=0
	    break



#create keypairs in all regions.
def create_key_pairs_all_regions():
    counter=0
    listLength=len(regionList)
    while(True):
        currentRegionName=regionList[counter]
        ec2 = boto3.resource('ec2',region_name=currentRegionName)
	config_instances()
	counter=counter+1
	if(counter==listLength-1):
	    counter=0
	    break


#ec2 = boto3.resource('ec2',region_name="us-east-1") # resource is the original ec2. .

#create_key_pairs_all_regions()
#delete_all_keys()


#create the main program
regionIndex=0
regionIndexBefore=-1
regionlistLength=len(regionList)
while(True):
    regionRand=random.randint(regionIndex,regionlistLength-1) # get a random number between the region list length
    instancesRandNumber=random.randint(minInstances,maxInstances-1) # get a random number between the min max instances vars
    print instancesRandNumber
    ec2 = boto3.resource('ec2',region_name=regionList[regionRand]) # create ec2 var from the random region.
    currentImage=imageList[regionRand] # get the current image by using regionRand number
    if(regionIndexBefore!=regionRand):
        config_instances() # to create key pair we need the boto3.resource. to delete key pair we need the client.
        os.system('chmod 400 ec2keyInstance4.pem')
        print regionList[regionRand]
        terminate_instances() # before creating new instances - terminate all running instances
        print 'Creating instances'
        create_Multiinstances(instancesRandNumber) #create number of instances
        time.sleep(60)
        print 'commit'
        commit_instanceFromRegion() # check which instances are running and execute Automain code in it.
        regionIndexBefore=regionRand # save the last region index number
        time.sleep(random.randint(360,500))
        terminate_instances() # terminate all running instances
        ec3 = boto3.client('ec2',region_name=regionList[regionRand])
        delete_key_pair()
    



"""
def start_func():
    #create the main program
    regionIndex=0
    regionIndexBefore=-1
    regionlistLength=len(regionList)
    #while(True):
    regionRand=random.randint(regionIndex,regionlistLength) # get a random number between the region list length
    instancesRandNumber=random.randint(minInstances,maxInstances) # get a random number between the min max instances vars
    print instancesRandNumber
    ec2 = boto3.resource('ec2',region_name=regionList[regionRand]) # create ec2 var from the random region.
    currentImage=imageList[regionRand] # get the current image by using regionRand number
    if(regionIndexBefore!=regionRand):
        config_instances() # to create key pair we need the boto3.resource. to delete key pair we need the client.
        print regionList[regionRand]
        terminate_instances() # before creating new instances - terminate all running instances
        print 'Creating instances'
        create_Multiinstances(instancesRandNumber) #create number of instances
        print 'commit'
        commit_instanceFromRegion() # check which instances are running and execute Automain code in it.
        regionIndexBefore=regionRand # save the last region index number
        ec3 = boto3.client('ec2',region_name=regionList[regionRand])
        delete_key_pair()
    


def createThreads():
    instancesRandNumber=random.randint(minInstances,maxInstances) # get a random number between the min max instances vars
    for fred in range(1,instancesRandNumber):
	t=threading.Thread(start_func,args=())


def main():
   createThreads()


if __name__ == "__main__":
    main()
"""


#Tried to create and delete key pairs in different regions.
"""
counter=0
listLength=len(regionList)
while(True):
    currentRegionName=regionList[counter]
    currentImage=imageList[counter]
    ec2 = boto3.resource('ec2',region_name=currentRegionName)
    config_instances()
    create_instances()
    counter=counter+1
    #delete_key_pair()
    if(counter==listLength-1):
	counter=0
	delete_all_keys()
	break

"""


#Test to create instances and execute code.
"""
while(True):
    create_instances()
    time.sleep(100)
    #get_instances()
    hostIP=str(get_first_instance())
    print hostIP
    execute_command(hostIP)
    execute_command2(hostIP)
    execute_command3(hostIP)
    print 'test'
    time.sleep(400)
    #time.sleep(get_random(360,500))
    terminate_instances()
    time.sleep(100)
"""


