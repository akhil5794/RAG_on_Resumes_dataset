import os
from openai import OpenAI
import json
import tiktoken
from flask import Flask, request, jsonify, render_template

import parsing_given_resumes
from langchain.document_loaders import DirectoryLoader

directory = './resumes/'

def load_docs(directory):
    loader = DirectoryLoader(directory)
    documents = loader.load()
    return documents

documents = load_docs(directory)

if(len(documents) <= 0):
    print("---------No New Resumes detected----------")
else:
    print("There are ", len(documents), " new resumes detected")
    parsing_given_resumes.parse_new_resumes()


# In[8]:

def num_tokens_from_string(string: str, model: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = len(encoding.encode(string))
    return num_tokens


# Specify the path to the folder containing JSON files
folder_path = './parsed_resumes_json/'

# Function to load and process JSON files
def process_json_files(folder_path):
    # List all files in the folder
    files = os.listdir(folder_path)
    
    # List to store grouped JSON data
    grouped_json_data = []
    
    # Process files in groups of 5
    for i in range(0, len(files), 200):
        group_files = files[i:i+200]
        group_data = {}
        # Process each JSON file in the group
        for file in group_files:
            file_path = os.path.join(folder_path, file)
            if file.endswith('.json'):
                with open(file_path, 'r') as json_file:
                    # Load JSON data from the file
                    data = json.load(json_file)
                    # Add the data to the group_data dictionary with the file name as the key
                    group_data[file] = data
            elif file.endswith('.txt'):
                with open(file_path, 'r') as txt_file:
                    data = txt_file
                    group_data[file] = data
            else:
                pass

        # Add the group_data dictionary to the grouped_json_data list
        grouped_json_data.append(group_data)
    
    return grouped_json_data

# Load and group JSON data from the specified folder
grouped_json_data = process_json_files(folder_path)

print(len(grouped_json_data[0]))

# In[ ]:


app = Flask(__name__)

os.environ["OPENAI_API_KEY"] = "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"
#openai.api_key = "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"
client = OpenAI()


# Define the route for the chatbot interface
@app.route('/')
def index():
    return render_template('index.html')

# Define the route for processing user messages
@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    max_tokens = 128000
    engine = "gpt-4-1106-preview" #"gpt-3.5-turbo-1106",#"gpt-4-32k",
    output = ""
    # Call the OpenAI API to generate a response
    for i in grouped_json_data:
        #print(i)
        estimated_prompt_tokens = num_tokens_from_string(user_input, engine)
        estimated_input_tokens = num_tokens_from_string(str(i), engine)
        estimated_answer_tokens = 4096
        print("Given Prompt Tokens, Given Input Tokens, Max Answer Tokens, Overall Tokens: ", estimated_prompt_tokens, estimated_input_tokens, estimated_answer_tokens, max_tokens)

        response = client.chat.completions.create(
        model= "gpt-4-1106-preview", #"gpt-3.5-turbo-1106",#"gpt-4-32k",
        messages=[
        {
          "role": "system",
          "content": str(i)
        },
        {
          "role": "user",
          "content": user_input
        }
        ],
        temperature=0.1,
        seed=1189,
        max_tokens=4096
        )

        
        bot_response = response.choices[0].message.content.strip()
        output = output + bot_response + "**"
        print(bot_response)
    return jsonify({'bot_response': output})

if __name__ == '__main__':
    app.run(debug=True)


# In[ ]:


# # Define the query
# query = "Tell me the name of person(s) who has experience in Finance domain?"

# # Construct the prompt for ChatGPT


# # Send the prompt to ChatGPT and get its response


# In[ ]:


# answer = response.choices[0].message.content #response["choices"][0]["text"]
# print(answer)


# In[ ]:


# # Set your OpenAI API key here
# OPENAI_API_KEY = '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'
# openai.api_key = OPENAI_API_KEY

