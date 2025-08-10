import requests
from PySide6.QtCore import QThread, Signal
import json

# Thread for Ollama API calls
class OllamaThread(QThread):
    response_ready = Signal(str)
    error_occurred = Signal(str)
    
    def __init__(self, prompt, model_name="openchat"):
        super().__init__()
        self.prompt = prompt
        self.model_name = model_name
        self.url = "http://localhost:11434/api/chat" # Ollama API endpoint

    def run(self):
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "user", "content": self.prompt}
            ],
            "stream": False # Set to False for a single response; True for streaming
        }
        
        try:
            # Make a synchronous request. If you want streaming, this part
            # would need a more complex loop to read chunks.
            response = requests.post(self.url, json=payload, timeout=300) # Added timeout
            response.raise_for_status() # Raise an exception for bad status codes

            data = response.json()
            # Ollama's /api/chat endpoint returns a 'message' dictionary
            # within the top-level JSON object.
            ai_content = data.get("message", {}).get("content", "AI response not available.")
            
            self.response_ready.emit(ai_content)

        except requests.exceptions.ConnectionError:
            self.error_occurred.emit("Could not connect to Ollama server. Please ensure Ollama is running and the model is downloaded.")
        except requests.exceptions.Timeout:
            self.error_occurred.emit("Ollama request timed out. The model might be taking too long to respond.")
        except requests.exceptions.HTTPError as e:
            self.error_occurred.emit(f"Ollama HTTP error: {e.response.status_code} - {e.response.text}")
        except requests.exceptions.RequestException as e:
            self.error_occurred.emit(f"An unexpected error occurred with Ollama: {str(e)}")
        except json.JSONDecodeError:
            self.error_occurred.emit("Failed to decode JSON response from Ollama. Invalid response format.")
        except Exception as e:
            self.error_occurred.emit(f"An unknown error occurred in OllamaThread: {str(e)}")


# Fallback function if Ollama is not active or fails
def get_fallback_ai_response(message):
    """
    Provides a basic, non-Ollama AI response if the Ollama model is not available or fails.
    """
    if "hello" in message.lower():
        return "Hi there! How can I help you today?"
    elif "time" in message.lower():
        return "I don't have a real-time clock, but it's always time to code!"
    elif "help" in message.lower():
        return "I'm here to assist you with your coding tasks. What do you need help with?"
    else:
        return "I'm not sure how to respond to that. Can you please rephrase? (Ollama AI not active)"