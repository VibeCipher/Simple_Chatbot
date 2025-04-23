# Gemini AI Chatbot

A simple yet powerful command-line chatbot powered by Google's Gemini AI model. This chatbot features a beautiful terminal interface with markdown support, conversation history, and more.

## Features

- 🧠 Powered by Google's Gemini Pro model
- 💬 Persistent chat history between sessions
- 🎨 Beautiful terminal UI with Rich
- 📝 Markdown rendering for AI responses
- 🔐 Secure API key handling

- ## Installation
1. Clone this repository:
```
git clone https://github.com/yourusername/gemini-chatbot.git
cd gemini-chatbot
```
2. Install the required packages:
```
pip install -r requirements.txt
```
3. Get a Gemini API key from Google AI Studio

## Usage
Run the chatbot with your API key:
```
python gemini_chatbot.py --api-key YOUR_API_KEY
 ```
### Command-line Arguments
- --api-key YOUR_KEY : Provide your Gemini API key
- --new : Start a new conversation (ignore previous history)
- --list-models : List all available models
- --model MODEL_NAME : Specify which model to use (default: gemini-1.5-flash)

## Troubleshooting
If you encounter model-related errors:

1. Run with the --list-models flag to see which models are available with your API key
2. Specify a valid model with the --model flag
