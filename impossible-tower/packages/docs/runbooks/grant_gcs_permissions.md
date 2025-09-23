# Runbook: Granting Google Cloud Storage Permissions to a Service Account

This runbook provides instructions on how to grant the necessary permissions to a service account to access Google Cloud Storage (GCS) buckets.

## Prerequisites

*   Google Cloud SDK (gcloud) installed and configured.
*   `gsutil` command-line tool installed.
*   Owner or IAM Admin role on the Google Cloud project.

## Steps

1.  **Identify the service account:**

    *   The service account being used is `terraform@seven-l-prod.iam.gserviceaccount.com`.

2.  **Grant the Storage Object Viewer role:**

    *   This role allows the service account to list the contents of the bucket.
    *   Run the following command:

        ```bash
        gcloud projects add-iam-policy-binding <your-project-id> \
            --member="serviceAccount:terraform@seven-l-prod.iam.gserviceaccount.com" \
            --role="roles/storage.objectViewer"
        ```

        Replace `<your-project-id>` with your Google Cloud project ID.

3.  **Grant the Storage Object Admin role (if necessary):**

    *   This role allows the service account to read and write objects in the bucket.
    *   Run the following command:

        ```bash
        gcloud projects add-iam-policy-binding <your-project-id> \
            --member="serviceAccount:terraform@seven-l-prod.iam.gserviceaccount.com" \
            --role="roles/storage.objectAdmin"
        ```

        Replace `<your-project-id>` with your Google Cloud project ID.

## Verification

*   After granting the permissions, run the `gsutil ls gs://impossible-tower-data/` command to verify that the service account can now access the bucket.

## Additional Resources

*   [Google Cloud Storage Documentation](https://cloud.google.com/storage/docs)
*   [IAM Documentation](https://cloud.google.com/iam/docs)