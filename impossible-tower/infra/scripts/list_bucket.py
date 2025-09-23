from google.cloud import storage

def list_bucket_contents(bucket_name):
    """Lists the contents of a Google Cloud Storage bucket."""
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blobs = bucket.list_blobs()

        print(f"Contents of bucket {bucket_name}:")
        for blob in blobs:
            print(blob.name)

    except Exception as e:
        print(f"Error listing bucket contents: {e}")

if __name__ == "__main__":
    bucket_name = "impossible-tower-data"
    list_bucket_contents(bucket_name)