import json
import requests
import boto3

sqs = boto3.client('sqs')
queueUrl = "https://sqs.ap-southeast-1.amazonaws.com/294254988299/sam-test-stack-TaskQueue-4AVYU7NOA72I"  #修改为正确的SQS队列URL

s3 = boto3.client('s3')
bucketName = "dhgate-test"  #修改为正确的S3存储桶桶名


def lambda_handler(event, context):
    
    print(event)
    for record in event["Records"] :
        #processing message
        msg = json.loads(record['body'])
        print(msg['link'])
        link=msg['link']
        print(msg['key'])
        key=msg['key']
        
        #save image to /tmp
        tmpFileName = f"/tmp/{key}"
        r = requests.get(link, allow_redirects=True)
        open(tmpFileName, 'wb').write(r.content)
        print(tmpFileName)
        
        #upload image to s3
        response = s3.upload_file(tmpFileName, bucketName, key)
        print(response)
    
        #delete message if the process succeed
        receiptHandle = record['receiptHandle']
        response = sqs.delete_message(
            QueueUrl=queueUrl,
            ReceiptHandle=receiptHandle
        )
        print(response)

    return {
        "statusCode": 200,
        "body": ""
    }