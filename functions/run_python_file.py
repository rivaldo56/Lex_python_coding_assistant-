import os
import subprocess
from google.genai import types

def run_python_file(working_directory: str, file_path: str, args=[]):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_directory):
        return f'Cannot execute "{file_path}" as it is outside'
    if not os.path.isfile(abs_file_path):
        return f'File "{file_path}" not found'
    if not file_path.endswith(".py"):
        return f'Error:  "{file_path}" is not a Python file'
    
    try:
        final_args = ["python3", file_path]
        final_args.extend(args)
        output  = subprocess.run(
            final_args,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=abs_working_directory
        )
        final_string = f"""
        STDOUT:
        {output.stdout}
        STDERR:
        {output.stderr}
        """
        if output.stdout == "" and output.stderr == "":
            final_string = "No output produced.\n"
        if output.returncode != 0:
            final_string += f"Process exited with code {output.returncode}."
        return final_string
    except Exception as e:
        return f"Error:  executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="runs a Python3 interpreter. Accepts additional CLI args as an optional array.",
    parameters=types.Schema(
        type=types.Type.OBJECT,  
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to run, relative to the working directory. ",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                    description="Optional array of string arguments to pass to the script.",
                items=types.Schema(
                    type=types.Type.STRING
                    
                    )
            ),
        },
    ),
)