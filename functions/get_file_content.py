import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path: str):
    # Resolve working directory and file path
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(
        os.path.join(abs_working_directory, file_path)  # ✅ always relative to working_directory
    )

    if not abs_file_path.startswith(abs_working_directory):
        return {"error": f'"{file_path}" is outside the working dir'}
    if not os.path.isfile(abs_file_path):
        return {"error": f'"{file_path}" is not a file'}

    try:
        with open(abs_file_path, 'r', encoding="utf-8") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) >= MAX_CHARS:
                file_content_string += (
                    f' [..."{file_path}" truncated at {MAX_CHARS} characters]'
                )
        return {"content": file_content_string}
    except Exception as e:
        return {"error": f"Exception reading file: {e}"}


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the content of a specified file as a string, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)
