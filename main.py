from dotenv import load_dotenv
from src.nn.glaDos import GLaDOS

load_dotenv()

glados_dialogs = "./context/glados.txt"

if __name__ == "__main__":
    glados_ai = GLaDOS(glados_dialogs)

    print("GLaDOS консоль. Введите 'exit' для выхода.\n")

    while True:
        user_input = input("Вы: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("GLaDOS: Пока. Не возвращайтесь.")
            break
        
        answer = glados_ai.ask(user_input)
        print(f"GLaDOS: {answer}\n")
