"""
This script picks up PowerSchool tables and reports exported from the Data Export Manager to the ps_downloads directory Python Anywhere & delivers them to AWS S3
It requires the credentials_all.json to be in the main directory of Python Anywhere and contain the following
 - AWS Keys/Bucket Names
 - Python Anywhere Directory Path to ps_downloads
 ****Replace with code from ps_test_2.py when Simone has updated views.
"""
import os
import json
import boto3

def upload_to_s3(source_file, bucket_name, destination_path, access_key_id, access_secret_key):
    """ Function to move files to AWS S3 Bucket """
    s3 = boto3.resource('s3', aws_access_key_id=access_key_id, aws_secret_access_key=access_secret_key)
    s3.meta.client.upload_file(source_file, bucket_name, destination_path)

def clean_header(header):
    split_header = header.rsplit('.', 1)
    if len(split_header) > 1:
        clean_header = split_header[1]
    else:
        clean_header = split_header[0]
    clean_header = clean_header.lower().replace(' ', '_')
    # print("Cleaned header (after lowercasing and replacing spaces):", clean_header)
    return clean_header


def process_headers(headers):
    """ function to move field names through the clean_header function """
    cleaned_headers = []
    for header in headers:
        cleaned_header = clean_header(header)
        cleaned_headers.append(cleaned_header)
    return cleaned_headers
    print("Processed Headers:" , cleaned_headers)

def main(config_path, csv_file, source_directory):
    # Load AWS credentials and file paths from a configuration file
    with open(config_path) as config_file:
        config = json.load(config_file)
        aws_config = config["awss3"]
    csv_file_path = os.path.join(source_directory, csv_file)
    access_key_id = aws_config["access_key_id"]
    access_secret_key = aws_config["access_secret_key"]
    s3_bucket_name = aws_config["bucket_name"]
    sub_folder = aws_config["powerschool_bucket"]

    # Read headers from CSV file and clean them
    with open(csv_file_path, 'r') as file:
        headers = file.readline().strip().split(',')
        cleaned_headers = process_headers(headers)

    # Write cleaned headers back to the CSV file
    with open(csv_file_path, 'r+') as file:
        content = file.readlines()
        file.seek(0)
        file.write(','.join(cleaned_headers) + '\n')
        file.writelines(content[1:])  # Write the rest of the file content after the header line

    # Upload the CSV file to AWS S3
    aws_path = sub_folder + '/' + csv_file
    upload_to_s3(csv_file_path, s3_bucket_name, aws_path, access_key_id, access_secret_key)
    print(f"{csv_file} moved to S3: {sub_folder}")


if __name__ == "__main__":
    CONFIG_FILE_PATH = "/home/KIPPNashvilleData/credentials_all.json"

    # Extract source_directory from the configuration file
    with open(CONFIG_FILE_PATH) as config_file:
        config = json.load(config_file)
        source_directory = config["python_paths"]["ps_directory"]

    # Use source_directory in the loop
    csv_files = [file for file in os.listdir(source_directory) if file.endswith(".csv")]

    # Loop the files in the directory through the function.
    for csv_file in csv_files:
        main(CONFIG_FILE_PATH, csv_file, source_directory)
