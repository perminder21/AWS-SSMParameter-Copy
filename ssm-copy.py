#!/usr/bin/env python3
#
# Copy SSM Parameter Store values to a new path.
#
# Designed to work with Python 3.6 and up. Only external dependency is boto3.
#
# Call: copy-ssm-ps-path.py source-tree-name target-tree-name new-kms-uuid
#

import os
import sys

import boto3


def main(args):
    if len(args) != 3:
        sys.stderr.write("Invalid args.\n")
        sys.exit(1)

    source_path = args[1]
    target_path = args[2]

    ssm = boto3.client("ssm")
    paginator = ssm.get_paginator("get_parameters_by_path")
    for page in paginator.paginate(Path=f"/{source_path}/", WithDecryption=True):
        for parameter in page["Parameters"]:
            raw_key = parameter["Name"]
            key_name = os.path.basename(raw_key)
            new_name = f"/{target_path}/{key_name}"
            ssm.put_parameter(
                Name=new_name,
                Value=parameter["Value"],
                Type="SecureString",
            )
            sys.stderr.write(f"Copied {key_name} from {source_path} to {target_path}.\n")


if __name__ == "__main__":
    main(sys.argv)
