import os
import json
import time
from datetime import datetime
import google.generativeai as genai
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich import print
from rich.prompt import Prompt
import argparse

# Initialize Rich console for better formatting
console = Console()

def list_available_models(api_key):
    """List all available models for the given API key"""
    genai.configure(api_key=api_key)
    try:
        models = genai.list_models()
        console.print("[bold yellow]Available Models:[/bold yellow]")
        for model in models:
            console.print(f"- {model.name}")
        return models
    except Exception as e:
        console.print(f"[bold red]Error listing models: {e}[/bold red]")
        return []

def setup_gemini(api_key, model_name="gemini-1.5-flash"):
    """Configure the Gemini API with your API key"""
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name)

def load_chat_history(filename="chat_history.json"):
    """Load previous chat history if it exists"""
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            console.print("[bold red]Error loading chat history. Starting fresh.[/bold red]")
    return []

def save_chat_history(history, filename="chat_history.json"):
    """Save the current chat history to a file"""
    with open(filename, "w") as f:
        json.dump(history, f, indent=2)

def format_response(text):
    """Format the AI response using Rich's markdown renderer"""
    return Markdown(text)

def main():
    parser = argparse.ArgumentParser(description="Gemini-powered AI Chatbot")
    parser.add_argument("--api-key", help="Your Gemini API key")
    parser.add_argument("--new", action="store_true", help="Start a new chat session")
    parser.add_argument("--list-models", action="store_true", help="List available models")
    parser.add_argument("--model", default="gemini-1.5-flash", help="Model to use (default: gemini-1.5-flash)")
    args = parser.parse_args()
    
    # Get API key from arguments or environment variable or prompt
    api_key = args.api_key or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        api_key = Prompt.ask("Enter your Gemini API key", password=True)
    
    # List models if requested
    if args.list_models:
        list_available_models(api_key)
        return
    
    # Setup the model
    try:
        model = setup_gemini(api_key, args.model)
        console.print(Panel.fit(f"[bold green]Gemini AI Chatbot[/bold green] (Using model: {args.model})\n[italic]Type 'exit' to quit, 'save' to save the conversation, or 'clear' to start fresh[/italic]"))
    except Exception as e:
        console.print(f"[bold red]Error initializing Gemini: {e}[/bold red]")
        console.print("[yellow]Try running with --list-models to see available models[/yellow]")
        return
    
    # Load chat history unless --new flag is used
    history = [] if args.new else load_chat_history()
    
    # Create a chat session
    chat = model.start_chat(history=[
        {"role": "user" if msg["role"] == "user" else "model", "parts": [msg["content"]]}
        for msg in history
    ])
    
    # Display previous chat if it exists
    if history and not args.new:
        console.print("[bold yellow]--- Previous Conversation ---[/bold yellow]")
        for msg in history:
            if msg["role"] == "user":
                console.print(f"[bold blue]You:[/bold blue]")
                console.print(msg["content"])
            else:
                console.print(f"[bold green]AI:[/bold green]")
                console.print(format_response(msg["content"]))
        console.print("[bold yellow]--- New Conversation ---[/bold yellow]")
    
    # Main chat loop
    while True:
        user_input = Prompt.ask("\n[bold blue]You[/bold blue]")
        
        # Handle special commands
        if user_input.lower() == "exit":
            save_chat_history(history)
            console.print("[bold yellow]Conversation saved. Goodbye![/bold yellow]")
            break
        elif user_input.lower() == "save":
            save_chat_history(history)
            console.print("[bold green]Conversation saved![/bold green]")
            continue
        elif user_input.lower() == "clear":
            history = []
            chat = model.start_chat()
            console.print("[bold yellow]Chat history cleared![/bold yellow]")
            continue
        elif user_input.lower() == "list models":
            list_available_models(api_key)
            continue
        
        # Add user message to history
        history.append({"role": "user", "content": user_input, "timestamp": datetime.now().isoformat()})
        
        # Display typing animation
        with console.status("[bold green]AI is thinking...[/bold green]", spinner="dots"):
            try:
                response = chat.send_message(user_input)
                response_text = response.text
            except Exception as e:
                console.print(f"[bold red]Error: {e}[/bold red]")
                continue
        
        # Add AI response to history
        history.append({"role": "assistant", "content": response_text, "timestamp": datetime.now().isoformat()})
        
        # Display AI response
        console.print("\n[bold green]AI:[/bold green]")
        console.print(format_response(response_text))

if __name__ == "__main__":
    main()