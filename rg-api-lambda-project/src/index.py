import json
import boto3
import os

ec2 = boto3.client('ec2')
dynamodb = boto3.resource('dynamodb')
#table = dynamodb.Table(os.environ['TABLE_NAME'])
table = dynamodb.Table('rg-test-api-lambda-dynamodb')
#API_KEY = os.environ['API_KEY']

def lambda_handler(event, context):
    path = event['resource']
    method = event['httpMethod']
    try:
        cidr_block = event.get('body').get('cidr_block')
        subnet_cidrs = event.get('body').get('subnet_cidrs')
    except AttributeError:
        cidr_block = None
        subnet_cidrs = None

    if path == "/create" and method == "POST":
        return create_vpc(cidr_block, subnet_cidrs)
    elif path == "/vpcs" and method == "GET":
        return list_vpcs()
    elif path == "/delete" and method == "POST":
        return delete_vpcs()
    else:
        return response(404, {"error": "Not found"})

def create_vpc(cidr_block, subnet_cidrs):
    try:
        vpc = ec2.create_vpc(CidrBlock=cidr_block,
        TagSpecifications = [
            {
                'ResourceType': 'vpc',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'rg-test-vpc'
                    }
                ]
            }
        ]
        )
        vpc_id = vpc['Vpc']['VpcId']

        ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsSupport={'Value': True})
        ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsHostnames={'Value': True})

        subnet_ids = []
        for cidr in subnet_cidrs:
            subnet = ec2.create_subnet(CidrBlock=cidr, VpcId=vpc_id)
            subnet_ids.append(subnet['Subnet']['SubnetId'])

        table.put_item(Item={
            'vpc_id': vpc_id,
            'cidr_block': cidr_block,
            'subnet_ids': subnet_ids
        })

        return response(200, {"vpc_id": vpc_id, "subnet_ids": subnet_ids})

    except Exception as e:
        return response(500, {"error": str(e)})

def list_vpcs():
    try:
        dynamodb = boto3.resource('dynamodb', region_name="us-east-2")
        dynamodb_table = dynamodb.Table('rg-test-api-lambda-dynamodb')
        items = dynamodb_table.scan()
        return response(200, items)
    except Exception as e:
        return response(500, {"error": str(e)})

def delete_vpcs():
    try:
        dynamodb = boto3.resource('dynamodb', region_name="us-east-2")
        dynamodb_table = dynamodb.Table('rg-test-api-lambda-dynamodb')
        items = dynamodb_table.scan()
        for item in items['Items']:
            vpc_id = item['vpc_id']
            ec2_resource = boto3.resource('ec2')
            vpc_resources = ec2_resource.Vpc(vpc_id)
            for subnet in vpc_resources.subnets.all():
                print(f"Deleting subnet: {subnet.id}")
                #subnet.delete()
            print(f"Deleting vpc: {vpc_id}")
            #ec2.delete_vpc(VpcId=vpc_id)
            #dynamodb_table.delete_item(Key={'vpc_id': vpc_id})
        return response(200, items)
    except Exception as e:
        return response(500, {"error": str(e)})


def response(code, body):
    return {
        "statusCode": code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }