import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from typing import Optional
from tqdm import tqdm

class IdeaGenerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print("🌀 Загрузка модели генерации...")
        with tqdm(total=100) as pbar:
            self.tokenizer = GPT2Tokenizer.from_pretrained("sberbank-ai/rugpt3small_based_on_gpt2")
            pbar.update(50)
            self.model = GPT2LMHeadModel.from_pretrained("sberbank-ai/rugpt3small_based_on_gpt2").to(self.device)
            pbar.update(50)

    def generate_idea(self, prompt: str, max_length: int = 100) -> Optional[str]:
        """Генерация текста на основе промпта"""
        try:
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                num_return_sequences=1,
                do_sample=True,  # Добавьте эту строку
                temperature=0.9,
                top_k=50,
                pad_token_id=self.tokenizer.eos_token_id
            )
            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        except Exception as e:
            print(f"🚨 Ошибка генерации: {str(e)}")
            return None

    def brainstorm(self, context: dict) -> list:
        """Генерация идей с учетом контекста (эмоции, памяти и т.д.)"""
        prompt = f"Контекст: {context.get('description', '')}\nИдеи:"
        idea = self.generate_idea(prompt)
        return [idea] if idea else []