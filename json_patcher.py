import argparse
import json
import os
import re
import logging

LOG_PATH = 'json_patcher.log'

def log_feature(status, file_path, message):
    logging.basicConfig(filename=LOG_PATH, level=logging.INFO, format='%(message)s')
    log_message = f"{status} {file_path}: {message}"
    logging.info(log_message)

def log_message_replacements(file_path, feature_type, old, new, count):
    status = 'INFO' if count > 0 else 'WARNING'
    message = f"{feature_type} {count} occurrences. {repr(old)} -> {repr(new)}"
    log_feature(status, file_path, message)

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
    parser.add_argument('workspace', help='Workspace path')
    parser.add_argument('--json_path', default='json_patcher.json', help='Path to json_patcher.json')
    parser.add_argument('--output_dir', help='Common output directory')
    args = parser.parse_args()

    try:
        with open(args.json_path) as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        logging.error(f"JSON file does not exist: {args.json_path}")
        return
    
    # Loop through all files in json_patcher.json
    for file_info in data['json_patcher']:
        input_file_path = os.path.join(args.workspace, file_info['path'], file_info['filename'])

        # Verify input file exists
        if not os.path.isfile(input_file_path):
            log_feature('ERROR', input_file_path, 'File not found')
            continue
        else:
            # Get output path: if output_path is defined in json_patcher.json, otherwise use args.output_dir, otherwise use input file path
            # Priorities: output_path > args.output_dir > input file path
            output_dir = file_info.get('output_path') or args.output_dir or file_info['path']

            # Get output filename: if output_filename is defined in json_patcher.json, otherwise use input filename
            # Priorities: output_filename > input filename
            output_filename = file_info.get('output_filename', file_info['filename'])

            output_file_path = os.path.join(args.workspace, output_dir, output_filename)
            perform_replacements(input_file_path, file_info['features'], output_file_path)

if __name__ == "__main__":
   # Clear log file 
    with open(LOG_PATH, 'w'):
        pass

    main()