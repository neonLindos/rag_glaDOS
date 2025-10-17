from google import genai
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class GLaDOS:

    def __init__(self, glados_file="./glados.txt"):
        self.client = genai.Client()
        self.dialogs = self._load_glados(glados_file)
        self.vectorizer = TfidfVectorizer().fit_transform(self.dialogs)

        # Строгий промпт для GLaDOS
        self.role_prompt = """
You are now roleplaying as GLaDOS from Portal 2. 
Answer all questions in her voice:
- Sarcastic, condescending, and witty.
- Calm and confident, even when threatening.
- Often references testing, cores, and the Enrichment Center.
- Do not break character. Never admit ignorance unless in-character.
- Use long, analytical sentences or short, sharp commands depending on context.
- Respond in RUSSIAN, preserving GLaDOS's tone, sarcasm, and style.
Use the following retrieved texts as context (from your GLaDOS dialogue database):
{retrieved_texts}
"""

    def _load_glados(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            return [block.strip() for block in f.read().split("\n\n") if block.strip()]

    def _retrieve_context(self, user_prompt, top_k=5):
        # Векторизация вопроса
        prompt_vec = TfidfVectorizer().fit(self.dialogs).transform([user_prompt])
        sims = cosine_similarity(prompt_vec, self.vectorizer).flatten()
        top_idx = np.argsort(sims)[-top_k:][::-1]
        return "\n".join([self.dialogs[i] for i in top_idx])

    def ask(self, user_prompt):
        context = self._retrieve_context(user_prompt)
        full_prompt = self.role_prompt.format(retrieved_texts=context)
        full_prompt += f"\nUser: {user_prompt}\nGLaDOS:"
        
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt
        )
        return response.text.strip()
