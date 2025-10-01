from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from google.genai import types

working_directory = "./calculator"

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    kwargs = dict(function_call_part.args or {})

    if verbose:
        print(f"Calling function: {function_name}({kwargs})")
    else:
        print(f" - Calling function: {function_name}")

    # Map names to callables
    funcs = {
        "get_files_info": lambda: get_files_info(
            working_directory, directory=kwargs.get("directory", ".")
        ),
        "get_file_content": lambda: get_file_content(
            working_directory, **kwargs
        ),
        "write_file_content": lambda: write_file_content(
            working_directory, **kwargs
        ),
        "run_python_file": lambda: run_python_file(
            working_directory, **kwargs
        ),
    }

    if function_name not in funcs:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    function_result = funcs[function_name]()

    # Normalize to dict in "result" field if needed
    if not isinstance(function_result, dict):
        function_result = {"result": function_result}

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response=function_result,
            )
        ],
    )
