
from typing import Any, Dict, List, Optional
import time
from rich.console import Console

console = Console()

class ServiceError(Exception):
    pass

class BaseService:
    def __init__(self, name: str):
        self.name = name

    def get_metadata(self) -> Dict[str, Any]:
        return {}

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

class HFService(BaseService):
    def __init__(self, model_name: str, price_per_token: float, max_new_tokens: int = 32):
        super().__init__("hf")
        self.model_name = model_name
        self.price_per_token = price_per_token
        self.max_new_tokens = max_new_tokens
        self.model = None
        self.tokenizer = None
        self.device = None
        # We do NOT load immediately here to avoid blocking construction
        # The caller should call load_async

    def load_sync(self):
        """Blocking load."""
        self._load_model()

    def _load_model(self):
        console.log(f"[yellow]🤖 Loading model '{self.model_name}'... (This may take a while)[/yellow]")
        try:
            from .hf import load_model_and_tokenizer
            self.model, self.tokenizer, self.device = load_model_and_tokenizer(self.model_name)
            console.log(f"[green]✓ Model '{self.model_name}' loaded successfully[/green]")
        except ImportError:
            raise ServiceError("transformers not installed")
        except Exception as e:
            raise ServiceError(f"Failed to load model: {e}")

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "models": [self.model_name],
            "price_per_token": self.price_per_token,
            "max_new_tokens": self.max_new_tokens
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        if not self.model:
            raise ServiceError("Model not loaded")
        
        prompt = params.get("prompt")
        max_new = int(params.get("max_new_tokens", self.max_new_tokens))
        
        if not prompt:
            raise ServiceError("Missing prompt")

        try:
            t0 = time.time()
            from .hf import generate_text
            text = generate_text(self.model, self.tokenizer, self.device, prompt, max_new)
            
            # Token accounting
            in_tokens = len(self.tokenizer.encode(prompt))
            out_tokens = len(self.tokenizer.encode(text))
            new_tokens = max(0, out_tokens - in_tokens)
            latency_ms = int((time.time() - t0) * 1000.0)
            cost = self.price_per_token * new_tokens
            
            return {
                "text": text,
                "tokens": new_tokens,
                "latency_ms": latency_ms,
                "price_per_token": self.price_per_token,
                "cost": cost
            }
        except Exception as e:
            raise ServiceError(str(e))
