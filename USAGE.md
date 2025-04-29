# Local Lorekeeper Setup Guide

This guide will walk you through the steps to get the Local Lorekeeper application running on your personal computer. It's designed to be as straightforward as possible, even if you're not familiar with software development.

## What You Need (Prerequisites)

Before you start, you'll need a few things installed on your computer:

1.  **Python:** This is the programming language the application is built with. You need Python version 3.7 or higher.
    *   **How to get it:** Download from the official Python website: [https://www.python.org/downloads/](https://www.python.org/downloads/). Follow the installation instructions for your operating system (Windows, macOS, Linux). Make sure to check the option that says "Add Python to PATH" during installation on Windows.

2.  **Ollama:** This software allows you to run large language models (the AI part) directly on your computer, without needing an internet connection after the initial setup. It's essential for the Lorekeeper's AI features.
    *   **How to get it:** Download from the official Ollama website: [https://ollama.com/](https://ollama.com/). Follow the installation instructions for your operating system.
    *   **Important:** After installing Ollama, you need to download an AI model. Open your computer's terminal or command prompt and run the command `ollama run llama2` (or another preferred model like `mistral`). This will download the AI model. You only need to do this once.

3.  **Project Files:** The code and resources for the Local Lorekeeper application.
    *   **How to get it:** You likely received a zip file (`local-lorekeeper.zip`). Extract this zip file to a folder on your computer (e.g., in your Documents or Desktop folder). This folder will be your project directory.

## Step-by-Step Setup

Once you have the prerequisites installed and the project files extracted, follow these steps:

1.  **Open Your Terminal or Command Prompt:**
    *   On Windows, search for "Command Prompt" or "PowerShell".
    *   On macOS or Linux, search for "Terminal".

2.  **Navigate to the Project Folder:**
    *   In the terminal, use the `cd` command to go into the folder where you extracted the project files.
    *   For example, if you extracted it to a folder named `local-lorekeeper` on your Desktop, you might type:
        ```bash
        cd Desktop/local-lorekeeper
        ```
    *   *(Tip: You can often drag and drop the project folder into the terminal window after typing `cd ` (with a space) to get the correct path.)*

3.  **Install Project Dependencies:**
    *   The project needs some additional components (libraries) to run. These are listed in the `requirements.txt` file.
    *   In the terminal, while inside the project folder, run the command:
        ```bash
        pip install -r requirements.txt
        ```
    *   *(This command tells Python to install all the necessary libraries listed in the requirements file. This might take a few moments.)*

4.  **Configure the Application (Optional but Recommended):**
    *   There's a file named `.env` in the project folder. This file is used for settings, like specifying which Ollama AI model the application should use.
    *   Open the `.env` file in a simple text editor (like Notepad on Windows, TextEdit on macOS, or any code editor).
    *   You might see lines like `OLLAMA_MODEL=llama2`. You can change `llama2` to the name of the model you downloaded with Ollama if it's different.
    *   Save and close the file.
    *   *(If the `.env` file is empty or doesn't exist, you can create it and add the line `OLLAMA_MODEL=llama2` to use the Llama 2 model.)*

## Running the Application

Now that everything is set up, you can start the Local Lorekeeper:

1.  Open your terminal or command prompt again and navigate to the project folder (if you closed it).
2.  Run the main application script using Python:
    ```bash
    python app.py
    ```
3.  The application should start, and after a moment, it will typically open a new tab in your web browser with the Local Lorekeeper interface.

## Accessing the Application

The application runs locally on your computer and is accessed through your web browser. The address will usually look something like `http://localhost:8501`.

*   Keep the terminal window running while you are using the application. Closing the terminal will stop the application.

## Troubleshooting

*   **"command not found: python" or "command not found: pip":** Make sure Python was installed correctly and that you checked the "Add Python to PATH" option during installation (on Windows). You might need to restart your terminal or computer after installing Python.
*   **Errors during `pip install`:** Check your internet connection. If errors persist, there might be a compatibility issue or a problem with a specific library. (For HR purposes, this might be a point where technical assistance is needed).
*   **Application doesn't open in browser:** Look at the output in the terminal. It usually provides the local web address (URL) where the application is running. Copy and paste that URL into your browser.
*   **AI features not working:** Ensure Ollama is running and that you have downloaded an AI model using `ollama run <model_name>`.

If you encounter significant issues, providing the output from the terminal to someone with technical expertise will be helpful for diagnosis.
