from orchestrator import Orchestrator


def main():
    print("=" * 60)
    print("ORQUESTRADOR DE AGENTES")
    print("Gerador de aplicações usando agentes de IA")
    print("=" * 60)

    request = input("\nDescreva a aplicação que você quer criar:\n\n> ")

    orchestrator = Orchestrator()
    result = orchestrator.run(request)

    print("\n" + "=" * 60)
    print("PROCESSO FINALIZADO")
    print("=" * 60)

    print(f"\nIterações realizadas: {result['iterations']}")

    print("\nArquivos:")
    for filename in result["files"]:
        print(f"{filename}")


if __name__ == "__main__":
    main()