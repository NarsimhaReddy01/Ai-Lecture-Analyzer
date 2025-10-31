from dotenv import load_dotenv
import os, boto3, uuid

# ✅ Load .env from project root
load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))

aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
bucket_name = os.getenv("AWS_STORAGE_BUCKET_NAME")
region = os.getenv("AWS_S3_REGION_NAME", "us-east-1")

print("AWS_ACCESS_KEY_ID:", aws_access_key)
print("AWS_SECRET_ACCESS_KEY:", aws_secret_key)
print("AWS_STORAGE_BUCKET_NAME:", bucket_name)
print("AWS_S3_REGION_NAME:", region)

if not all([aws_access_key, aws_secret_key, bucket_name]):
    print("❌ Missing AWS credentials. Check your .env file.")
    exit(1)

# ✅ Initialize S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=region
)

# ✅ Test upload
try:
    key = f"test_upload_{uuid.uuid4()}.txt"
    s3.put_object(Bucket=bucket_name, Key=key, Body="This is a test upload.")
    print(f"✅ Uploaded test object: s3://{bucket_name}/{key}")
except Exception as e:
    print("❌ Upload failed:", e)
