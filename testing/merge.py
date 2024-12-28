import os

def merge_python_files(project_dir, output_file):
    """
    Merges all Python files in the given project directory into a single text file.

    :param project_dir: The root directory of the project to scan.
    :param output_file: The file where the merged content will be saved.
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as outfile:
            # Include main.py from parent directory
            main_file_path = os.path.join(os.path.dirname(project_dir), 'main.py')
            if os.path.exists(main_file_path):
                with open(main_file_path, 'r', encoding='utf-8') as mainfile:
                    outfile.write(f"# File: {main_file_path}\n")
                    outfile.write(mainfile.read())
                    outfile.write("\n\n")

            # Include all Python files from the project directory
            for root, _, files in os.walk(project_dir):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            outfile.write(f"# File: {file_path}\n")
                            outfile.write(infile.read())
                            outfile.write("\n\n")
        print(f"All Python files have been merged into {output_file}.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Replace 'your_project_directory' with the path to your project
    project_directory = "../src"
    output_filename = "merged_code.py"

    merge_python_files(project_directory, output_filename)
