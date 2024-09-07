import os
from openai import OpenAI
import re
import json
import tiktoken
from langchain.document_loaders import DirectoryLoader
import json
import datetime
import shutil


def parse_new_resumes():
    # Specify the source and destination folders
    parsed_resumes = 'parsed_successfully'
    failed_resumes = 'failed_to_parse'

    os.environ["OPENAI_API_KEY"] = "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"
    #openai.api_key = "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"
    client = OpenAI()


    # In[3]:


    prompt_questions = """Summarize the text below into a JSON with the following structure {basic_info: {first_name, last_name, full_name, email, summary, skills, phone_number, location, portfolio_website_url, linkedin_url, github_main_page_url, university, education_level (BS, MS, or PhD), graduation_year, graduation_month, majors, GPA}, work_experience: [{job_title, company, location, duration}], project_experience:[{project_name, project_description}]}"""


    # In[4]:


    directory = './resumes/'

    def load_docs(directory):
        loader = DirectoryLoader(directory)
        documents = loader.load()
        return documents

    documents = load_docs(directory)
    print("The number of documents are: ", len(documents))


    # In[6]:


    # See: https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb

    def num_tokens_from_string(string: str, model: str) -> int:
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.encoding_for_model(model)
        num_tokens = len(encoding.encode(string))
        return num_tokens


    # In[7]:


    def query_completion(input_string: str, prompt: str,
                        engine: str = 'gpt-3.5-turbo-1106',
                        temperature: float = 0.0,
                        top_p: int = 1,
                        frequency_penalty: int = 0,
                        max_tokens: int = 4097,
                        presence_penalty: int = 0) -> object:
        """
        Base function for querying GPT-3. 
        Send a request to GPT-3 with the passed-in function parameters and return the response object.
        :param prompt: GPT-3 completion prompt.
        :param engine: The engine, or model, to generate completion.
        :param temperature: Controls the randomnesss. Lower means more deterministic.
        :param max_tokens: Maximum number of tokens to be used for prompt and completion combined.
        :param top_p: Controls diversity via nucleus sampling.
        :param frequency_penalty: How much to penalize new tokens based on their existence in text so far.
        :param presence_penalty: How much to penalize new tokens based on whether they appear in text so far.
        :return: GPT-3 response object
        """
        #logger.info(f'query_completion: using {engine}')

        estimated_prompt_tokens = num_tokens_from_string(prompt, engine)
        estimated_input_tokens = num_tokens_from_string(input_string, engine)
        estimated_answer_tokens = (max_tokens - estimated_prompt_tokens - estimated_input_tokens)
        print("Prompt Tokens, Input Tokens, Answer Tokens, Overall Tokens: ", estimated_prompt_tokens, estimated_input_tokens, estimated_answer_tokens, max_tokens)

        if(estimated_input_tokens <= 2400):
            response = client.chat.completions.create(
            model=engine,
            messages=[
            {
              "role": "system",
              "content": input_string
            },
            {
              "role": "user",
              "content": prompt
            }
            ],  
            temperature=temperature,
            #max_tokens=estimated_answer_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty
            )
            return response
        else:
            print("The resume length is too huge, check the resume once")


    # In[8]:


    def query_resume(prompt_questions : str, pdf_str: str) -> dict:
        """
        Query GPT-3 for the work experience and / or basic information from the resume at the PDF file path.
        :param pdf_path: Path to the PDF file.
        :return dictionary of resume with keys (basic_info, work_experience).
        """
        resume = {}
        #pdf_str = self.pdf2string(pdf_path)
        #print(pdf_str)


        #prompt = prompt_questions + ':\n' + pdf_str

        # Reference: https://platform.openai.com/docs/models/gpt-3-5
        engine = 'gpt-3.5-turbo-1106'
        max_tokens = 4097

        response = query_completion(prompt=prompt_questions,input_string = pdf_str,engine=engine, max_tokens = max_tokens)
        response_text = response.choices[0].message.content.strip()#response['choices'][0]['text'].strip()
        # Add double quotes around keys using regular expressions
        response_text = re.sub(r'(\w+):', r'"\1":', response_text)
        # Find the first "{" and last "}" positions
        #start_index = response_text.find("{")
        #end_index = response_text.rfind("}")
        #response_text = response_text[start_index:]

        #print(response_text)
        try:
            resume = json.loads(response_text)
        except:
            resume = str(response_text)
        #print(resume)
        return resume


    # In[9]:


    #all_resumes = {}
    for i in documents:
        pdf_str = list(i)[1][1]
        file_name = list(i)[2][1]['source']

        # Split the file path using "\\" as the delimiter
        parts = file_name.split("resumes\\")
        # Get the last part of the split string and split it using "." as the delimiter
        file_name_parts = parts[-1].split(".")
        # Get the desired file name without the extension
        file_name_parts = file_name_parts[0]

        try:
            op = query_resume(prompt_questions=prompt_questions, pdf_str=pdf_str)
            if type(op) is str:
                # Open the file in write mode ('w')
                with open('./parsed_resumes_json/'+file_name_parts+'.txt', 'w') as file:
                    # Write the string to the file
                    file.write(op)
            else:
                op["file_name"] = parts[-1]
                with open('./parsed_resumes_json/'+file_name_parts+'.json', 'w') as json_file:
                    json.dump(op, json_file)

            # Move the file from the source folder to the destination folder
            shutil.move(os.path.join('resumes', parts[-1]), os.path.join(parsed_resumes, parts[-1]))

            #all_resumes[op["basic_info"]["full_name"]] = op
            print("Parsing Successful: ", list(i)[2])
            print("-------------------------------")
        except Exception as e: 
            print(e)
            print("Some error in: ", list(i)[2])
            # Move the file from the source folder to the destination folder
            shutil.move(os.path.join('resumes', parts[-1]), os.path.join(failed_resumes, parts[-1]))
            print("-------------------------------")