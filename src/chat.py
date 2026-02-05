from search import search_prompt


def main():
    print("Faça sua pergunta (digite 'sair' para encerrar):")
    while True:
        pergunta = input("\nPERGUNTA: ")
        if pergunta.strip().lower() in ["sair", "exit", "quit"]:
            print("Encerrando chat.")
            break
        resposta = search_prompt(pergunta)
        print(f"RESPOSTA: {resposta}\n")

if __name__ == "__main__":
    main()