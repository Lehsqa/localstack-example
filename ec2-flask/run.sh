#!/bin/bash

export AWS_ENDPOINT_URL="http://localhost:4566"

aws ec2 create-key-pair \
    --key-name key \
    --query 'KeyMaterial' \
    --output text | tee key.pem

chmod 400 key.pem

aws ec2 authorize-security-group-ingress \
    --group-id default \
    --protocol tcp \
    --port 8000 \
    --cidr 0.0.0.0/0

sg_id=$(aws ec2 describe-security-groups | jq -r '.SecurityGroups[0].GroupId')

aws ec2 run-instances \
    --image-id ami-ff0fea8310f3 \
    --count 1 \
    --instance-type t3.nano --key-name key \
    --security-group-ids $sg_id \
    --user-data file://user_script.sh

list_instances=$(aws ec2 describe-instances | jq -r '.Reservations[0].Instance[0].InstanceId')

aws ec2 terminate-instances --instance-ids $list_instances
