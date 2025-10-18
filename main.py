from dotenv import load_dotenv
from src.nn.glaDos import GLaDOS
from src.nn.langchain_genimi import LangchainGlaDOS

load_dotenv()

glados_dialogs = "./context/glados_dialogs.txt"
lore_path = "./context/hl_portal_lore.txt"


def landchain_GlaDos():
    glados = LangchainGlaDOS(
        dialogs_path=glados_dialogs,
        lore_path=lore_path
    )
    # Создаем базу знаний, если она еще не создана
    glados.build_knowledge_base()
    
    print("GLaDOS консоль (Langchain). Введите 'exit' для выхода.\n")
    
    while True:
        user_input = input("Вы: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("GLaDOS: Серьезно? Уже уходите? Ну, это было... увлекательно.")
            break
        
        glados.run(query=user_input)


def simple_glaDOS():    
    glados_ai = GLaDOS(glados_dialogs)

    print("GLaDOS консоль. Введите 'exit' для выхода.\n")

    while True:
        user_input = input("Вы: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("GLaDOS: Пока. Не возвращайтесь.")
            break
        
        answer = glados_ai.ask(user_input)
        print(f"GLaDOS: {answer}\n")


if __name__ == "__main__":
    landchain_GlaDos()
    # Для запуска simple_glaDOS раскомментируйте следующую строку
    # simple_glaDOS()