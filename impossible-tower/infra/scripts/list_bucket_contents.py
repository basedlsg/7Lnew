#!/usr/bin/env python3
"""
Script to list contents of Google Cloud Storage buckets.
Lists the contents of specific GCS buckets using gcloud storage ls command.
"""

import subprocess
import sys
import logging
import os
from typing import List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bucket_listing.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Activate service account
try:
    logger.info("Setting active account to carlos@raxverse.com")
    result = subprocess.run(
        ['gcloud', 'config', 'set', 'account', 'carlos@raxverse.com'],
        capture_output=True,
        text=True,
        check=True
    )
    logger.info("Successfully set active account")
except subprocess.CalledProcessError as e:
    error_msg = f"Failed to set active account: {e.stderr.strip()}"
    logger.error(error_msg)
    print(f"Error setting active account: {e.stderr.strip()}")
    sys.exit(1)
except Exception as e:
    error_msg = f"Unexpected error setting active account: {str(e)}"
    logger.error(error_msg)
    print(f"Unexpected error setting active account: {str(e)}")
    sys.exit(1)

# List of GCS buckets to list contents for
BUCKETS = [
    'gs://impossible-tower-data/itower/2025-09-19/',
    'gs://impossible-tower-data/itower/2025-09-19/synth_50/',
    'gs://impossible-tower-data/itower/v0.1/synth_500'
]

def list_bucket_contents(bucket_url: str) -> bool:
    """
    List contents of a GCS bucket using gcloud storage ls command.

    Args:
        bucket_url (str): The GCS bucket URL to list contents for

    Returns:
        bool: True if successful, False if error occurred
    """
    try:
        logger.info(f"Listing contents of bucket: {bucket_url}")

        # Set GOOGLE_APPLICATION_CREDENTIALS environment variable
        gcp_credentials_path = '/Users/carlos/NOUS/secure_keys/gcp_credentials.json'
        my_env = os.environ.copy()
        my_env['GOOGLE_APPLICATION_CREDENTIALS'] = gcp_credentials_path

        # Execute gcloud storage ls command
        result = subprocess.run(
            ['gcloud', 'storage', 'ls', bucket_url, '--project=plannyc-12345'],
            capture_output=True,
            text=True,
            check=True,
            env=my_env
        )

        # Print the bucket header
        print(f"\n{'='*60}")
        print(f"Contents of {bucket_url}")
        print(f"{'='*60}")

        # Print the output
        if result.stdout.strip():
            print(result.stdout)
        else:
            print("No contents found in this bucket.")

        logger.info(f"Successfully listed contents of bucket: {bucket_url}")
        return True

    except subprocess.CalledProcessError as e:
        error_msg = f"Failed to list contents of bucket {bucket_url}: {e.stderr.strip()}"
        logger.error(error_msg)
        print(f"Error listing {bucket_url}: {e.stderr.strip()}")
        return False
    except Exception as e:
        error_msg = f"Unexpected error listing bucket {bucket_url}: {str(e)}"
        logger.error(error_msg)
        print(f"Unexpected error listing {bucket_url}: {str(e)}")
        return False

def main():
    """Main function to list contents of all specified buckets."""
    logger.info("Starting bucket contents listing script")
    print("Google Cloud Storage Bucket Contents Listing")
    print("=" * 50)

    # Check authentication environment
    print(f"\n{'='*60}")
    print("AUTHENTICATION ENVIRONMENT DEBUG")
    print(f"{'='*60}")

    # Check GOOGLE_APPLICATION_CREDENTIALS environment variable
    import os
    gcp_credentials = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    if gcp_credentials:
        print(f"GOOGLE_APPLICATION_CREDENTIALS: {gcp_credentials}")
    else:
        print("GOOGLE_APPLICATION_CREDENTIALS: Not set")

    # Run gcloud auth list command
    print(f"\n{'-'*40}")
    print("Running 'gcloud auth list' command:")
    print(f"{'-'*40}")

    try:
        auth_result = subprocess.run(
            ['gcloud', 'auth', 'list', '--project=plannyc-12345'],
            capture_output=True,
            text=True,
            check=True
        )
        print(auth_result.stdout)
        logger.info("Successfully ran gcloud auth list command")
    except subprocess.CalledProcessError as e:
        error_msg = f"Failed to run gcloud auth list: {e.stderr.strip()}"
        logger.error(error_msg)
        print(f"Error running gcloud auth list: {e.stderr.strip()}")
    except Exception as e:
        error_msg = f"Unexpected error running gcloud auth list: {str(e)}"
        logger.error(error_msg)
        print(f"Unexpected error running gcloud auth list: {str(e)}")

    success_count = 0
    total_buckets = len(BUCKETS)

    for bucket_url in BUCKETS:
        if list_bucket_contents(bucket_url):
            success_count += 1

    # Print summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Total buckets processed: {total_buckets}")
    print(f"Successful listings: {success_count}")
    print(f"Failed listings: {total_buckets - success_count}")

    logger.info(f"Script completed. Success rate: {success_count}/{total_buckets}")

    # Exit with appropriate code
    if success_count == total_buckets:
        print("\nAll bucket listings completed successfully!")
        logger.info("All bucket listings completed successfully")
        sys.exit(0)
    else:
        print(f"\nSome bucket listings failed. Check logs for details.")
        logger.warning(f"Some bucket listings failed: {total_buckets - success_count} failures")
        sys.exit(1)

if __name__ == "__main__":
    main()