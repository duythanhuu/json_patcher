"""
Author: Duy Than Huu
Date: 03-June-2024
Description:
    This script is used to patch JSON files based on the configuration file
    'json_patcher.json'. The script reads the configuration file and applies
    the specified replacements, inserts, and regex replacements to the JSON
    files. The script logs the changes made to the JSON files and saves the
    patched files in the specified output directory.  

Parameters:
    workspace (Mandatory): The path to the workspace where the JSON files are located.
    json_path (Optional): The path to the configuration file 'json_patcher.json'.
    output_dir (Optional): The common output directory where the patched JSON files will be saved.

Usage:
    python json_patcher.py workspace [--json_path JSON_PATH] [--output_dir OUTPUT_DIR]

"""
import argparse
import json
import os
import re
import logging
import glob

WORKSPACE_PATH = r"D:\workspace\dev_tools\json_patcher\json_patcher\sample_workspace"
JSON_PATCHER_PATH = 'json_patcher.json'
OUTPUT_DIR = 'output_test'
LOG_PATH = 'json_patcher.log'

""" Log feature to log file """
def log_feature(status, file_path, message):
    logging.basicConfig(filename=LOG_PATH, level=logging.INFO, format='%(message)s')
    log_message = f"{status} {file_path}: {message}"
    logging.info(log_message)

""" Log message for replacements """
def log_message_replacements(file_path, feature_type, old, new, count):
    status = 'INFO' if count > 0 else 'WARNING'
    message = f"{feature_type} {count} occurrences. {repr(old)} -> {repr(new)}"
    log_feature(status, file_path, message)

""" Find all files in current directory and subdirectories and return a list of file absolute paths with the specified extension"""
def find_files(directory, glob_pattern):
    file_input_absolute_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if glob.fnmatch.fnmatch(file, glob_pattern):
                file_input_absolute_paths.append(os.path.join(root, file))
    return file_input_absolute_paths

""" Perform replacements """
def perform_replacements(input_file_path, features, output_file_path):
    with open(input_file_path, 'r') as file:
        content = file.read()

        # Perform replacements
        for old, new in features['replacements'].items():
            content, count = re.subn(re.escape(old), new, content)
            log_message_replacements(input_file_path, 'replacements', old, new, count)
        
        # Perform inserts after string
        for existing, insert in features['inserts_afterstring'].items():
            content, count = re.subn(re.escape(existing), existing + insert, content)
            log_message_replacements(input_file_path, 'inserts_afterstring', existing, insert, count)
        
        # Perform inserts before string
        for existing, insert in features['insert_beforestring'].items():
            content, count = re.subn(re.escape(existing), insert + existing, content)
            log_message_replacements(input_file_path, 'insert_beforestring', existing, insert, count)
        
        # Perform regex replacements
        for pattern, replacement in features['regex_replacements'].items():
            content, count = re.subn(pattern, replacement, content)
            log_message_replacements(input_file_path, 'regex_replacements', pattern, replacement, count)

    # Create output directories if they do not exist
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    
    with open(output_file_path, 'w') as file:
        file.write(content)

def main():
    parser = argparse.ArgumentParser(description='JSON Patcher')
    parser.add_argument('--workspace', default=WORKSPACE_PATH, help='Workspace path')
    parser.add_argument('--json_path', default=JSON_PATCHER_PATH, help='Path to json_patcher.json')
    parser.add_argument('--output_dir', default=OUTPUT_DIR, help='Common output directory')
    args = parser.parse_args()

    try:
        with open(args.json_path) as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        logging.error(f"JSON file does not exist: {args.json_path}")
        return
    file_input_absolute_paths = []
    # Loop through all configs in json_patcher.json
    for file_info in data['json_patcher']:
        # Check path for input is provided in json_patcher.json
        if 'path' in file_info:
            act_input_folder_relative_path = file_info['path']
        else:
            log_feature('WARNING', 'path', 'Path not found, working with root workspace path.')
            act_input_folder_relative_path = ""
        act_input_folder_absolute_path = os.path.join(args.workspace, act_input_folder_relative_path)

        # Check path for output is provided in json_patcher.json
        # Priorities: output_path(json) > output_dir(argument) > input path
        if 'output_path' in file_info:
            act_output_folder_relative_path = file_info['output_path']
        elif (args.output_dir):
            act_output_folder_relative_path = args.output_dir
        else:
            act_output_folder_relative_path = ""
        act_output_folder_absolute_path = os.path.join(args.workspace, act_output_folder_relative_path)

        # Check if output_filename is provided in json_patcher.json
        # Priorities: output_filename(json) > input filename
        if 'output_filename' not in file_info:
            output_filename = ""
        else:
            output_filename = file_info['output_filename']

        # Check if a specific filename is provided in json_patcher.json
        # If filename is a list, find all files in the current directory and subdirectories
        if isinstance(file_info['filename'], list):
            file_input_absolute_paths = []
            for ele_filename in file_info['filename']:
                if '*' in ele_filename:
                    file_input_absolute_paths.extend(find_files(act_input_folder_absolute_path, ele_filename))
                else:
                    file_input_absolute_paths.append(os.path.join(act_input_folder_absolute_path, ele_filename))
        # If filename is a string, find the file in the current directory
        else:
            file_input_absolute_paths = os.path.join(file_info['path'],[file_info['filename']])

        # Loop through all files in the list
        for file_input_absolute_paths in file_input_absolute_paths:
            input_file_path = file_input_absolute_paths

            # Verify input file exists
            if not os.path.isfile(input_file_path):
                log_feature('ERROR', input_file_path, 'File not found')
                continue
            else:
                if output_filename == "":
                    output_file_path = os.path.join(act_output_folder_absolute_path, os.path.basename(input_file_path))
                else:
                    output_file_path = os.path.join(act_output_folder_absolute_path, output_filename)
                perform_replacements(input_file_path, file_info['features'], output_file_path)

if __name__ == "__main__":
   # Clear log file 
    with open(LOG_PATH, 'w'):
        pass

    main()