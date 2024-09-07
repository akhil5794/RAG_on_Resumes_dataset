# RAG on Resumes Dataset using OPENAI and Langchain

## STEP 1
# README for Resume Parsing Python Script

## Overview
This Python script is designed to parse resumes from PDF/txt/doc(x)/other files and extract relevant information, such as personal details, work experience, and project experience, using OpenAI’s GPT-3.5 model. The script reads resumes from a specified directory, processes them using the GPT model, and outputs the extracted information in JSON format. The resumes that are parsed successfully are moved to a success folder, and failed ones are moved to a failure folder.

## Requirements

### Python Packages
You will need the following Python libraries:
- `openai`: For interacting with the OpenAI GPT model.
- `os`: For file system operations.
- `re`: For handling regular expressions.
- `json`: For working with JSON data.
- `tiktoken`: To handle token encoding.
- `langchain`: To load and handle resume documents.
- `datetime`: For handling date-related tasks.
- `shutil`: For moving files between directories.

Install the required libraries using:

```bash
pip install openai tiktoken langchain
```

### OpenAI API Key
Make sure to set your OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY='your-api-key'
```

## File Structure

The script uses the following folder structure:
- `resumes/`: The directory where the PDF resumes are stored.
- `parsed_resumes_json/`: The directory where successfully parsed resumes are saved in JSON format.
- `parsed_successfully/`: Directory where successfully parsed resumes are moved.
- `failed_to_parse/`: Directory where resumes that failed to parse are moved.

## How to Use

1. **Place Resumes in the `resumes/` Directory**  
   Ensure that the resumes you want to parse are in PDF format and placed inside the `resumes/` directory.

2. **Run the Script**  
   The script parses all the resumes in the `resumes/` directory using the OpenAI GPT-3.5 model to extract relevant information.

   ```bash
   python parse_resumes.py
   ```

3. **Process Resumes**  
   The script loads the resumes, sends the text to the GPT model using a predefined prompt, and expects a JSON structure in response. The extracted JSON data is saved in the `parsed_resumes_json/` folder. Each resume is then moved to either the `parsed_successfully/` or `failed_to_parse/` folder depending on the outcome.

## Key Functions

### `parse_new_resumes()`
- Main function that coordinates loading the resumes, querying GPT, saving output, and moving files based on success or failure.

### `load_docs(directory)`
- Loads the resume documents from the specified directory.

### `num_tokens_from_string(string, model)`
- Counts the number of tokens in a string for a given GPT model.

### `query_completion(input_string, prompt, engine, ...)`
- Queries the OpenAI API to get the completion result from GPT-3.5 based on the input string and prompt.

### `query_resume(prompt_questions, pdf_str)`
- Sends the resume text to GPT-3.5 and parses the result into a JSON format.

## Error Handling
If a resume fails to be parsed, it is moved to the `failed_to_parse/` directory, and an error message is printed.

## Output
Parsed resumes are saved as JSON files in the `parsed_resumes_json/` directory, with filenames corresponding to the original resume files.

## Example of JSON Output
```json
{
  "basic_info": {
    "first_name": "John",
    "last_name": "Doe",
    "full_name": "John Doe",
    "email": "johndoe@example.com",
    "skills": ["Python", "Machine Learning"],
    ...
  },
  "work_experience": [
    {
      "job_title": "Data Scientist",
      "company": "TechCorp",
      "duration": "2 years",
      ...
    }
  ],
  "project_experience": [
    {
      "project_name": "Project A",
      "project_description": "Worked on building models to predict..."
    }
  ]
}
```

## STEP 2

# README for Resume Parsing and Chatbot Interface using Flask

## Overview

This Python application parses resumes from PDF files, processes them using OpenAI's GPT models, and exposes a Flask web interface for interacting with the parsed data. The application groups parsed resumes into batches of 200 and allows users to query the data through a chatbot interface powered by GPT-4.

## Requirements

### Python Packages

You will need the following Python libraries:
- `openai`: For interacting with OpenAI's GPT models.
- `flask`: For creating a web interface and handling HTTP requests.
- `os`: For file system operations.
- `json`: For working with JSON data.
- `tiktoken`: For handling token encoding.
- `langchain`: For loading and handling resume documents.

Install the required libraries using:

```bash
pip install openai flask tiktoken langchain
```

### OpenAI API Key

Make sure to set your OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY='your-api-key'
```

## File Structure

The following folder structure is expected:
- `resumes/`: Directory where the resume PDF files are stored.
- `parsed_resumes_json/`: Directory where parsed resume JSON files are stored.
- `templates/index.html`: The HTML template for the chatbot interface.

## How to Use

### Step 1: Parsing Resumes

1. **Place resumes in the `resumes/` directory**.
2. **Run the script to parse resumes**: 
   The resumes will be processed, and the parsed data will be saved as JSON files in the `parsed_resumes_json/` directory.

   ```bash
   python app.py
   ```

### Step 2: Start the Flask Application

1. **Start the Flask application**:
   The application serves a chatbot interface and processes user input.

   ```bash
   python app.py
   ```

2. **Access the Web Interface**:
   Open a browser and navigate to `http://127.0.0.1:5000/`. You should see a chatbot interface.

### Step 3: Query the Resumes

- Enter your queries in the chatbot interface.
- The app will search the parsed resumes for relevant information using GPT-4 and return the results.

## Key Components

### `load_docs(directory)`
- Loads resume documents from the specified directory.

### `num_tokens_from_string(string, model)`
- Calculates the number of tokens for a given string and GPT model.

### `process_json_files(folder_path)`
- Groups parsed resume JSON files into batches of 200 for further processing.

### `get_response()`
- Processes user input from the chatbot interface, queries the grouped resume data using GPT-4, and returns the chatbot response.

### Flask Routes
- **`'/'`**: Displays the chatbot interface (HTML page).
- **`'/get_response'`**: Handles POST requests from the chatbot, processes the user input, and returns a GPT response.

## Example of JSON Data

The grouped JSON data follows this structure:

```json
{
    "basic_info": {
        "first_name": "Jane",
        "last_name": "Doe",
        "full_name": "Jane Doe",
        "email": "jane.doe@example.com",
        "skills": ["Python", "Data Science"],
        ...
    },
    "work_experience": [
        {
            "job_title": "Data Scientist",
            "company": "TechCorp",
            "duration": "3 years",
            ...
        }
    ],
    "project_experience": [
        {
            "project_name": "AI Model Development",
            "project_description": "Developed machine learning models to predict outcomes..."
        }
    ]
}
```

## Error Handling

- If there are no resumes in the `resumes/` directory, the script prints a message and terminates.
- If an error occurs during the OpenAI API call or JSON parsing, the error is caught and logged.

## Notes

- The API key is hard-coded in the script for development purposes. In production, store API keys securely in environment variables.
- The token limit for GPT models is respected; resumes longer than 4096 tokens will not be processed.

## Troubleshooting

- Ensure the OpenAI API key is correctly set as an environment variable.
- Verify the resume directory (`resumes/`) contains valid PDF files for parsing.

---

This README provides instructions for setting up, running, and using the application. For advanced use cases, you may modify the script to handle different input formats or add more detailed error handling.

## Notes
- The OpenAI API has a token limit, so resumes longer than 2400 tokens may fail to process.
- The API key is hard-coded in the script. It’s recommended to securely store the API key in environment variables.

---
