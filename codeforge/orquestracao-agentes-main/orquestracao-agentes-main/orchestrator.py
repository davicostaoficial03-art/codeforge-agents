from agent import Agent
from tools import save_generated_code

MAX_ITERATIONS = 3


class Orchestrator:

    def __init__(self):
        self.planner = Agent("planner")
        self.coder = Agent("coder")
        self.reviewer = Agent("reviewer")

    def run(self, request):
        print("\n" + "=" * 60)
        print("ETAPA 1 - PLANEJAMENTO")
        print("=" * 60)

        plan = self.planner.run(task=request)
        print(plan)

        code = None
        review = None
        files = []

        for iteration in range(MAX_ITERATIONS):
            print("\n" + "=" * 60)
            print(f"ETAPA 2 - CODIFICAÇÃO (ITERACAO {iteration + 1})")
            print("=" * 60)

            context = f"""
PLANO:

{plan}

CÓDIGO ANTERIOR:

{code or "Nenhum código foi criado ainda."}

REVISÃO ANTERIOR:

{review or "Nenhuma revisão foi realizada ainda."}
"""

            code = self.coder.run(task=request, context=context)
            print(code)

            files = save_generated_code(code)

            print("\nArquivos criados:")
            for filename in files:
                print(f" {filename}")

            print("\n" + "=" * 60)
            print("ETAPA 3 - REVISÃO")
            print("=" * 60)

            review = self.reviewer.run(task=request, context=code)
            print(review)

            if "APPROVED: YES" in review.upper():
                print("\nAplicação aprovada!")

                return {
                    "plan": plan,
                    "code": code,
                    "review": review,
                    "files": files,
                    "iterations": iteration + 1
                }

            print("\nA aplicação precisa de correções.")

        return {
            "plan": plan,
            "code": code,
            "review": review,
            "files": files,
            "iterations": MAX_ITERATIONS
        }