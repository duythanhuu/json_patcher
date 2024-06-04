# JSON Patcher

JSON Patcher is a Python script that performs various string manipulations on files based on instructions provided in a JSON file.

## Features

- Replacements: Replace all occurrences of a string with another string.
- Inserts after string: Insert a string after all occurrences of another string.
- Inserts before string: Insert a string before all occurrences of another string.
- Regex replacements: Replace all matches of a regular expression with a string.

## Install library

To install the required libraries for this project, navigate to the project directory in your terminal and run the following command:

```bash
pip install -r requirements.txt
```

## Usage

1. Prepare a JSON file with the following structure:

```json
{
    "json_patcher": [
                {
            "path": "dummy\\libs",
            "filename": ["dummy_lib.c", "*.cpp"],
            "features": {
                "replacements": {
                    "#include <stdio.h>": "//replace here \n#include <stdio.h>",
                    "int main() {": "//replace 2 here \nint main() {",
                    "have to be failed": "//replace 2 here \nint main() {"
                },
                "inserts_afterstring": {
                    "FILE *file;": "// inserts_afterstring here",
                    "char ch;": "// inserts_afterstring here"
                },
                "insert_beforestring": {
                    "putchar(ch);": "// insert_beforestring here \nputchar(ch);",
                    "ch = fgetc(file);": "// insert_beforestring here \nch = fgetc(file);"
                },
                "regex_replacements": {
                    "0x.*?;": "0xFF // regex_pattern1"
                }
            }
        },
        {
            "path": "dummy/include",
            "filename": ["dummy_not_here.h"],
            "output_path": "output",
            "output_filename": "new_dummy_without_output_path.h",
            "features": {
                "replacements": {
                    "#ifndef DUMMY_H": "#ifndef DUMMY_H // replacement 1",
                    "#define DUMMY_H": "#define DUMMY_H // replacement 2",
                    "one more failed": "#define DUMMY_H // replacement 2"
                },
                "inserts_afterstring": {
                    "// Function declarations": " insert_afterstring1"
                },
                "insert_beforestring": {
                    "void printHello();": "// insert_beforestring1 \nvoid printHello();"
                },
                "regex_replacements": {
                }
            }
        }
    ]
}
```
- `path`: This is the relative path to the file to be processed, relative to the workspace.

- `filename`: This is the name of the file to be processed or the list of files or glob pattern.

- `output_path`: This is the relative path to the output folder. If it's blank or does not exist the new output file will store in same directory with input.

- `output_filename`: This is the name of the output file if you config for only one `filename` above.

- `features`: This is an object that specifies the string manipulations to be performed. It can contain the following properties:
    - `replacements`: An object where each key-value pair represents a string to be replaced and its replacement.
    - `inserts_afterstring`: An object where each key-value pair represents a string and a string to be inserted after it.
    - `inserts_beforestring`: An object where each key-value pair represents a string and a string to be inserted before it.
    - `regex_replacements`: An object where each key-value pair represents a regular expression and its replacement.

- `output_path`: This is the relative path to the output directory, relative to the workspace. If it is given in json the `--output_dir` you parsed will be ignored.

- `output_filename`: This is the name of the output file. If omitted, the script will use the original filename.


2. Run the script with the following command:

```bash
python json_patcher.py "workspace_path" --json_path="json_patcher.json" --output_dir="output_directory"
```

- `workspace_path`: This is the path to the workspace. This argument is mandatory. The workspace is the directory that contains the files to be processed.

- `--json_path`: This is the path to the JSON file that contains the instructions for the string manipulations. This argument is optional. If omitted, the script will look for a file named `json_patcher.json` in the current directory.

- `--output_dir`: This is the common output directory. This argument is optional. If it was not parsed and `output_path` does not exist in json, output direction will be same with input direction.


## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) and our [Code of Conduct](CODE_OF_CONDUCT.md) for details on how to participate in our community.

## License

JSON Patcher is licensed under the [MIT License](LICENSE.md).

## Contact

If you have any questions, feel free to [open an issue](https://github.com/duythanhuu/json_patcher/issues/new) or contact us directly.

## Acknowledgements

Thanks to all our [contributors](https://github.com/duythanhuu/json_patcher/graphs/contributors)!