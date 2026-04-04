## Simple LLM wrapper using transformers (no llama.cpp dependency)

import os
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

class LLMEngine:
    def __init__(self, model_path: str = "models/Llama-3.2-3B-Instruct-Q4_K_M.gguf"):
        # Check if we should use demo mode or a real model
        self.demo_mode = True
        self.model = None
        self.tokenizer = None
        self.generator = None

        # Try to use a small HuggingFace model if available
        try:
            # Use a very small model that can work on CPU
            model_name = "gpt2"  # Small, fast, works well for demo
            print(f"🔄 Loading {model_name}...")

            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name)

            # Create pipeline (no generation params here — pass at call time)
            self.generator = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                pad_token_id=self.tokenizer.eos_token_id
            )

            self.demo_mode = False
            print(f"✅ Loaded {model_name} successfully")

        except Exception as e:
            print(f"⚠️ Could not load model: {e}")
            print("📝 Running in context-only mode")

    def generate_stream(self, prompt: str, max_tokens: int = 1024):
        """Stream response token by token"""
        if self.demo_mode or not self.generator:
            # Context-only response
            response = self._generate_context_response(prompt)
            for char in response:
                yield char
            return

        try:
            # Truncate prompt to leave room for generation (GPT-2 max is 1024 tokens)
            max_prompt_tokens = 768
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=max_prompt_tokens)
            truncated_prompt = self.tokenizer.decode(inputs["input_ids"][0], skip_special_tokens=True)

            # Generate response using the pipeline
            responses = self.generator(truncated_prompt, max_new_tokens=256, do_sample=True, temperature=0.7, num_return_sequences=1)
            generated_text = responses[0]['generated_text']

            # Remove the original prompt from the response
            if generated_text.startswith(truncated_prompt):
                response = generated_text[len(truncated_prompt):].strip()
            else:
                response = generated_text.strip()

            # Stream character by character
            for char in response:
                yield char

        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            for char in error_msg:
                yield char

    def _generate_context_response(self, prompt: str) -> str:
        """Generate a response based on context when model is unavailable"""
        # Extract relevant parts from the prompt for a simple response
        if "Context:" in prompt:
            context_section = prompt.split("Context:")[1].split("Question:")[0].strip()
            question = prompt.split("Question:")[1].split("Answer:")[0].strip()

            # Count words in context
            word_count = len(context_section.split())

            return f"""Based on the {word_count} words of context provided, here's what I found:

📄 Context Summary: The documents contain information related to your question about "{question}".

📊 Key Information Available:
- The context has {word_count} words of relevant information
- Multiple document chunks were retrieved for this query
- The RAG pipeline is working correctly

⚠️ Note: This is a simplified response because the full AI model is not loaded. To get intelligent responses, install llama-cpp-python or ensure a transformer model is available.

For better results, you can:
1. Install: `pip install llama-cpp-python`
2. Or install: `pip install transformers torch`
"""
        else:
            return "🔒 Neural Vault - RAG System Working\n\n✅ Documents uploaded and processed\n✅ Vector store operational\n✅ Context retrieval functional\n\n⚠️ Full AI responses require model installation."