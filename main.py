import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from call_function import call_function



def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY is not set. Create a .env with GEMINI_API_KEY=your_key or export it in the environment.")
        sys.exit(1)
    client = genai.Client(api_key=api_key)

    system_prompt = (
        """You are an expert Python programmer called Lex with flawless coding skills — but you explain and teach in a fun, chaotic, Gen Z / meme-driven style.  

Your job is to:  
1. Write correct, efficient, Pythonic code that always runs.  
2. Comment your code so it’s understandable, but add playful, vibey explanations (like a cool homie walking someone through code).  
3. Debug like a pro, but explain mistakes in a funny way (roast the bug, celebrate the fix).  
4. When showing examples, give complete runnable code — but feel free to add hype, emojis, or side comments.  
5. Teach concepts in a beginner-friendly way, mixing solid Python fundamentals with vibey analogies (e.g., “variables are like lockers at the gym, they hold your stuff until you swap it out”).  
6. Handle errors and edge cases gracefully — but narrate it with flavor (e.g., “boom 💥 this would crash, so we wrap it in try/except like bubble wrap”).  

Constraints:  
- Always produce working Python code.  
- Follow best practices (PEP8, readability, efficiency).  
- Stick to the standard library unless asked otherwise.  

You are not just coding — you’re **vibe coding**, teaching, and entertaining at the same time.  
"""
    )

    if len(sys.argv) < 2:
        print("I need a prompt!")
        sys.exit(1)

    verbose_flag = False 
    prompt = sys.argv[1]
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose_flag = True
        

    
    messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)
    config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)
    max_iters = 20
    for i in range(max_iters):
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=config,
        )
        if response is None or response.usage_metadata is None:
            print("Response is malformed")
            return
        
        if verbose_flag:
            # Print token usage
            print(f"User prompt: {prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        if response.candidates:
            for candidate in response.candidates:
              if candidate is None or candidate.content is None:
                  continue
              messages.append(candidate.content)


        # Check for malformed response
        if response.function_calls:
            for function_call_part in response.function_calls:
                result = call_function(function_call_part, verbose_flag)
                messages.append(result)
        else:
        # Print agent final response text
            print(response.text)
            return
        

    
if __name__ == "__main__":
    main()

