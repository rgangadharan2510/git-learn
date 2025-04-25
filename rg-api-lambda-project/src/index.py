# This is an AWS Lambda function that creates a VPC and subnets, lists VPCs, and deletes VPCs.

# import necessary libraries
import json
import boto3
import src.logutil as logutil
logger = logutil.getLogger()

ec2 = boto3.client('ec2')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('rg-test-api-lambda-dynamodb')

def lambda_handler(event, context):
    # get the data from the event
    logger.info("*** Starting Lambda function ***")
    path = event['resource']
    method = event['httpMethod']

    if path == "/create" and method == "POST":
        logger.info("*** This is a POST request to create a VPC ***")
        cidr_block = event.get('body').get('cidr_block')
        subnet_cidrs = event.get('body').get('subnet_cidrs')
        return create_vpc(cidr_block, subnet_cidrs)
    elif path == "/vpcs" and method == "GET":
        logger.info("*** This is a GET request to list VPCs ***")
        return list_vpcs()
    else:
        return response(404, {"error": "Not found"})

def create_vpc(cidr_block, subnet_cidrs):
    try:
        logger.info("*** Creating VPC ***")
        vpc = (ec2.create_vpc
        (
            CidrBlock=cidr_block,
            TagSpecifications =
        [
            {
                'ResourceType': 'vpc',
                'Tags':
                [
                    {
                        'Key': 'Name',
                        'Value': 'rg-test-vpc'
                    }
                ]
            }
        ]))
        vpc_id = vpc['Vpc']['VpcId']
        logger.info(f"*** VPC Created *** vpc_id: {vpc_id}")

        ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsSupport={'Value': True})
        ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsHostnames={'Value': True})

        subnet_ids = []
        for cidr in subnet_cidrs:
            logger.info("*** Creating Subnets ***")
            subnet = ec2.create_subnet(CidrBlock=cidr, VpcId=vpc_id)
            subnet_ids.append(subnet['Subnet']['SubnetId'])
        logger.info(f"*** Subnets Created *** subnet_ids: {subnet_ids}")
        logger.info("*** Updating DynamoDB ***")
        table.put_item(Item={
            'vpc_id': vpc_id,
            'cidr_block': cidr_block,
            'subnet_ids': subnet_ids
        })

        return response(200, {"vpc_id": vpc_id, "subnet_ids": subnet_ids})

    except Exception as e:
        logger.error("*** Error creating VPC or Subnets ***")
        return response(500, {"error": str(e)})

def list_vpcs():
    try:
        dynamodb_table = dynamodb.Table('rg-test-api-lambda-dynamodb')
        logger.info("*** Getting the items from dynamoDB ***")
        items = dynamodb_table.scan()
        return response(200, items)
    except Exception as e:
        logger.error("*** Error calling dynamoDB ***")
        return response(500, {"error": str(e)})

def response(code, body):
    logger.info("*** Exiting Program ***")
    return {
        "statusCode": code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }