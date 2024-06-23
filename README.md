# TalkGPT
Was not able to think any other cool name :D

## Table of Contents
- [TalkGPT](#talkgpt)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Testing](#testing)
  - [Rough Implementation Idea](#rough-implementation-idea)
  - [Assumptions Made](#assumptions-made)
  - [Scope for Improvements/ Known issues](#scope-for-improvements-known-issues)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/shekhuverma/TalkGPT.git
    cd TalkGPT
    ```
2. Create a virtual environment and activate it
   ```bash
   python -m venv venv
   ```
   Activate it using
   ```bash
   #on windows
   venv\Scripts\Activate
   #on linux
   source venv/Scripts/Activate
   ```
3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Configure the environment variables in the template.env file and rename it to
   .env
2. Run the CLI application:

    ```bash
    python cli.py
    ```

## Testing
All the tests are done using Pytest.

To run all the tests, run the following command

```bash
pytest tests
```

or you can use tox for testing and linting
```
tox
```
This will run all the tests, formats and lints the code using Ruff.

## Rough Implementation Idea

1) Get the data from Pyadio Input stream using callback -> pass the data to Deepgram and save the response in a queue.
2) Get the data from queue in another async loop and for each item in queue pass the data to LLM and return the LLM result into OpenAI speech to text.


## Assumptions Made
1) The OpenAI text to speech was only working best for the following settings.
    sample_rate=22050, chunk_size=2048


## Scope for Improvements/ Known issues
- [ ] Not able to exit cleanly at times.
- [ ] Add more test cases.
- [ ] Some performance metrics are not working as expected. Will try to fix them
- [ ] Seprate the user and dev dependencies (By using PDM or poetry)

**Note - Tested and developed on Windows machine on python version 3.12**