# List Bucket Contents Runbook

## Overview
This runbook describes how to use the `list_bucket_contents.py` script to list the contents of Google Cloud Storage buckets related to the Impossible Tower project.

## Purpose
The script lists the contents of three specific GCS buckets:
- `gs://impossible-tower-data/itower/2025-09-19/`
- `gs://impossible-tower-data/itower/2025-09-19/synth_50/`
- `gs://impossible-tower-data/itower/v0.1/synth_500`

## Prerequisites
- Google Cloud SDK (`gcloud`) must be installed and authenticated
- Appropriate permissions to access the GCS buckets
- Python 3.6+ installed

## Execution

### Method 1: Direct Python Execution
```bash
cd impossible-tower/infra/scripts
python3 list_bucket_contents.py
```

### Method 2: Using the Script Shebang (Linux/Mac)
```bash
cd impossible-tower/infra/scripts
chmod +x list_bucket_contents.py
./list_bucket_contents.py
```

## Output
The script will:
1. Display a header for each bucket being processed
2. Show the contents of each bucket
3. Provide a summary of successful/failed operations
4. Create a log file named `bucket_listing.log` with detailed execution information

## Error Handling
- The script includes comprehensive error handling for gcloud command failures
- Failed bucket listings will not stop the execution of subsequent buckets
- All errors are logged to both console and log file
- Exit code 0 indicates complete success, exit code 1 indicates some failures

## Logs
- Console output: Real-time progress and results
- Log file: `bucket_listing.log` in the script directory containing detailed execution logs

## Troubleshooting

### Authentication Issues
If you encounter authentication errors:
```bash
gcloud auth login
gcloud auth application-default login
```

### Permission Issues
Ensure your account has the necessary permissions:
```bash
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="user:YOUR_EMAIL" \
  --role="roles/storage.objectViewer"
```

### gcloud Not Found
If gcloud is not installed:
```bash
# Install Google Cloud SDK
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init
```

## Security Notes
- The script only performs read operations (list contents)
- No data modification or deletion occurs
- All access is logged for audit purposes

## Related Scripts
- `generate_bucket_contents.py` - Generates test data for GCS buckets
- `list_bucket.py` - Alternative bucket listing script
- `list_bucket.sh` - Shell script version of bucket listing