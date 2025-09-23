# Runbook: Resolving Google Cloud Storage Permissions Issues

This runbook provides instructions on how to resolve potential authentication or permission issues when accessing Google Cloud Storage (GCS) buckets.

## Prerequisites

*   Google Cloud SDK (gcloud) installed and configured.
*   `gsutil` command-line tool installed.

## Troubleshooting Steps

1.  **Verify gcloud installation:**

    *   Open a terminal and run `gcloud version`.
    *   If gcloud is not installed, follow the instructions on the Google Cloud website to install it.

2.  **Authenticate with Google Cloud:**

    *   Run `gcloud auth login` and follow the prompts to authenticate with your Google account.
    *   If you are using a service account, ensure that the `GOOGLE_APPLICATION_CREDENTIALS` environment variable is set to the path of your service account key file.

3.  **Set the active project:**

    *   Run `gcloud config set project <your-project-id>` to set the active project. Replace `<your-project-id>` with your Google Cloud project ID.

4.  **Verify gsutil configuration:**

    *   Run `gsutil config -l` to list the current gsutil configuration.
    *   Ensure that the correct project ID is configured.

5.  **Check bucket permissions:**

    *   Ensure that the user or service account has the necessary permissions to access the bucket.
    *   The `Storage Object Viewer` role is required to list bucket contents.
    *   The `Storage Object Admin` role is required to read and write objects in the bucket.
    *   You can grant permissions using the Google Cloud Console or the `gcloud iam` command.

6.  **Test bucket access:**

    *   Run `gsutil ls gs://<your-bucket-name>` to test bucket access. Replace `<your-bucket-name>` with the name of your bucket.
    *   If you still encounter permission errors, double-check the IAM roles and permissions for the user or service account.

## Additional Resources

*   [Google Cloud Storage Documentation](https://cloud.google.com/storage/docs)
*   [gsutil Documentation](https://cloud.google.com/storage/docs/gsutil)