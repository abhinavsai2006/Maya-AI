"""
Offline AI capabilities using local models.
Provides AI responses without internet connection using Ollama.
"""

import os
import json
from typing import Optional
import subprocess

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


class OfflineAI:
    """Offline AI using Ollama local models."""
    
    def __init__(self, model: str = "llama2"):
        """
        Initialize offline AI.
        
        Args:
            model: Ollama model to use (llama2, mistral, codellama, etc.)
        """
        self.model = model
        self.base_url = "http://localhost:11434"
        self.is_available = self._check_ollama()
    
    def _check_ollama(self) -> bool:
        """Check if Ollama is running."""
        if not REQUESTS_AVAILABLE:
            return False
        
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def ask(self, prompt: str, max_tokens: int = 500) -> Optional[str]:
        """
        Ask offline AI a question.
        
        Args:
            prompt: Question or prompt
            max_tokens: Maximum response length
            
        Returns:
            AI response or None on failure
        """
        if not self.is_available:
            print("[Offline AI] Ollama not running. Start with: ollama serve")
            return None
        
        try:
            # Prepare request
            data = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": max_tokens
                }
            }
            
            # Send request
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()
            else:
                print(f"[Offline AI] Error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"[Offline AI] Failed to get response: {e}")
            return None
    
    def list_models(self) -> list:
        """
        List available Ollama models.
        
        Returns:
            List of model names
        """
        if not self.is_available:
            return []
        
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [model["name"] for model in data.get("models", [])]
            return []
        except:
            return []
    
    def pull_model(self, model_name: str) -> bool:
        """
        Download a model from Ollama registry.
        
        Args:
            model_name: Name of model to download (e.g., "llama2", "mistral")
            
        Returns:
            True if successful, False otherwise
        """
        if not self.is_available:
            print("[Offline AI] Ollama not running")
            return False
        
        try:
            print(f"[Offline AI] Downloading {model_name}... This may take several minutes.")
            
            data = {"name": model_name, "stream": False}
            response = requests.post(
                f"{self.base_url}/api/pull",
                json=data,
                timeout=600  # 10 minutes timeout for download
            )
            
            if response.status_code == 200:
                print(f"[Offline AI] {model_name} downloaded successfully")
                return True
            else:
                print(f"[Offline AI] Failed to download {model_name}")
                return False
                
        except Exception as e:
            print(f"[Offline AI] Error downloading model: {e}")
            return False


# Global instance
_offline_ai: Optional[OfflineAI] = None


def get_offline_ai(model: str = "llama2") -> OfflineAI:
    """Get or create offline AI instance."""
    global _offline_ai
    if _offline_ai is None:
        _offline_ai = OfflineAI(model)
    return _offline_ai


def ask_offline(prompt: str, model: str = "llama2") -> Optional[str]:
    """
    Ask offline AI (convenience function).
    
    Args:
        prompt: Question or prompt
        model: Model to use
        
    Returns:
        AI response or None
    """
    ai = get_offline_ai(model)
    return ai.ask(prompt)


def setup_offline_mode() -> str:
    """
    Setup guide for offline mode.
    
    Returns:
        Setup instructions
    """
    return """To use offline AI mode:

1. Install Ollama:
   - Windows: Download from https://ollama.ai/download/windows
   - macOS: Download from https://ollama.ai/download/mac
   - Linux: curl -fsSL https://ollama.ai/install.sh | sh

2. Start Ollama service:
   - Windows/Mac: Ollama starts automatically after installation
   - Linux: Run 'ollama serve' in terminal

3. Download a model:
   - Run: ollama pull llama2
   - Or: ollama pull mistral
   - Or: ollama pull codellama

4. Test offline mode:
   - Maya will automatically use offline AI when available
   - Set MAYA_USE_OFFLINE=1 to force offline mode

Popular models:
- llama2 (7B): Fast, general purpose
- mistral (7B): Better quality, slightly slower
- codellama (7B): Best for code-related tasks
- llama2:13b: Higher quality, needs more RAM
"""
