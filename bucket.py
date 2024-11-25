import json
import boto3
import time

def lambda_handler(event, context):
    start_time = time.time()
    print(f"Received event: {json.dumps(event)}")

    source_bucket = event['source_bucket']
    destination_bucket = event['destination_bucket']
    file_key = event['file_key']

    s3 = boto3.client('s3')

    try:
        print(f"Starting file copy from {source_bucket} to {destination_bucket} for file: {file_key}")
        
        s3.copy_object(
            CopySource={'Bucket': source_bucket, 'Key': file_key},
            Bucket=destination_bucket,
            Key=file_key
        )

        elapsed_time = time.time() - start_time
        print(f"File copied successfully in {elapsed_time:.2f} seconds")
        
        return {
            'statusCode': 200,
            'body': json.dumps(f"File {file_key} transferred successfully in {elapsed_time:.2f} seconds.")
        }

    except Exception as e:
        print(f"Error copying file: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error copying file: {str(e)}")
        }
            