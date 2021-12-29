#!/bin/bash
queueUrl="https://sqs.ap-southeast-1.amazonaws.com/294254988299/sam-test-stack-TaskQueue-4AVYU7NOA72I"
msgCount=10

for ((i=1;i<=$msgCount;i++))
do
    link='https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?ixlib=rb-1.2.1&ixid=MnwxMjA3fDF8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1769&q=80'
    key="pic$i.jpg"
    msg=$(jq -n -r \
       --arg link $link \
       --arg key $key \
       '{link:$link, key:$key}')
    echo $msg
    aws sqs send-message --queue-url $queueUrl --message-body "$msg"
done
