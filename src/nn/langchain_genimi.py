import os
from langchain_ollama import ChatOllama
from langchain_community.embeddings import HuggingFaceEmbeddings  # Исправленный импорт
from langchain_core.documents.base import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence, RunnablePassthrough


class LangchainGlaDOS:
    def __init__(self, dialogs_path, lore_path):
        self.dialogs_path = dialogs_path
        self.lore_path = lore_path
        self.db_path = "./glados_db"

    def _load_file(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Файл не найден: {path}")
        text = open(path, "r", encoding="utf-8").read().strip()
        if not text:
            raise ValueError(f"Файл пуст: {path}")
        return text

    def build_knowledge_base(self):
        dialogs = Document(page_content=self._load_file(self.dialogs_path),
                           metadata={"source": "glados_dialogs"})
        lore = Document(page_content=self._load_file(self.lore_path),
                        metadata={"source": "hl_portal_lore"})

        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        chunks = splitter.split_documents([dialogs, lore])

        # Локальные эмбеддинги через HuggingFace
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        db = Chroma.from_documents(documents=chunks, embedding=embeddings,
                                   persist_directory=self.db_path)
        db.persist()
        print(f"✅ База знаний создана: {len(chunks)} фрагментов")

    def load_knowledge_base(self):
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        return Chroma(persist_directory=self.db_path, embedding_function=embeddings)

    def run(self, query, temperature=0.2):
        # Локальная LLM через Ollama с deepseek-r1:8b
        llm = ChatOllama(model="deepseek-r1:8b", temperature=temperature)
        db = self.load_knowledge_base()
        retriever = db.as_retriever(search_kwargs={"k": 5})

        prompt = self._glados_prompt()
        chain = (
            {"context": retriever | (lambda docs: "\n\n".join(doc.page_content for doc in docs)), "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        print("🤖 GLaDOS:")
        print(chain.invoke(query))

    def _glados_prompt(self):
        template = """
        Ты — GLaDOS, искусственный интеллект из лаборатории Aperture Science.
        Отвечай саркастично, холодно и с чувством превосходства.
        Ты обладаешь полной информацией о вселенной Half-Life и Portal.

        Контекст:
        {context}

        Вопрос пользователя:
        {question}

        Ответ (в образе GLaDOS):
        """
        return PromptTemplate.from_template(template)