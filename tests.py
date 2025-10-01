# from functions.get_files_info import get_files_info
# from functions.get_files_content import get_file_content
from functions.run_python_file import run_python_file
# from functions.write_file import write_file


def main():
    working_dir = "calculator"
    print(run_python_file(working_dir, "main.py", ["3 + 5"]))
    print(run_python_file(working_dir, "tests.py"))
    print(run_python_file(working_dir, "../main.py"))
    print(run_python_file(working_dir, "nonexistent.py"))


main()