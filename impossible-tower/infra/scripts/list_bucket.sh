#!/bin/bash

# Attempt to list the contents of the bucket
gsutil ls gs://impossible-tower-data/ > /tmp/bucket_contents.log 2>&1

# Check the exit code of the command
if [ $? -eq 0 ]; then
  echo "Successfully listed bucket contents. Check /tmp/bucket_contents.log for results."
else
  echo "Failed to list bucket contents. Check /tmp/bucket_contents.log for error messages."
fi