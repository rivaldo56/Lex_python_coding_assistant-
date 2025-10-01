import os
from google.genai import types 

def write_file(working_directory, file_path, content):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_directory):
        return {"error": f'"{file_path}" is outside the working dir'}

    parent_dir = os.path.dirname(abs_file_path)
    try:
        os.makedirs(parent_dir, exist_ok=True)  # only create if missing
    except Exception as e:
        return {"error": f"Could not create parent directories: {parent_dir} = {e}"}

    try:
        with open(abs_file_path, 'w') as f:
            f.write(content)
        return {
            "result": f'Successfully wrote to "{file_path}" ({len(content)} characters written)',
            "file": file_path,
            "content": content  # 👈 include  written content
        }
    except Exception as e:
        return {"error": f"Exception writing file: {file_path}, {e}"}

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrites an existing file or writes content to a new file if it doesn't exist (and creates any necessary parent directories safely), constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write, from the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file as a string.",
            ),
        },
        required=["file_path", "content"],
    ),
)

