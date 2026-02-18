import os
import boto3
from decouple import config

print("--- CLEANING BUCKET ---")

try:
    s3 = boto3.client(
        's3',
        endpoint_url=config('AWS_S3_ENDPOINT_URL'),
        aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
        region_name='us-east-1'
    )
    
    bucket_name = config('AWS_STORAGE_BUCKET_NAME')
    # List and delete in batches
    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket_name)

    count = 0
    for page in pages:
        if 'Contents' in page:
            for obj in page['Contents']:
                # Delete only legacy JPG/PNG files, keep the new WebP
                if obj['Key'].lower().endswith(('.jpg', '.jpeg', '.png')):
                     print(f"Deleting legacy: {obj['Key']}...") 
                     s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
                     count += 1
                if count % 50 == 0:
                    print(f"Deleted {count} files...")
    
    print(f"✅ Bucket emptied successfully. Deleted {count} objects.")

except Exception as e:
    print(f"❌ Error cleaning bucket: {e}")
