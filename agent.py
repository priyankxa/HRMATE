
from llm import create_llm
from rag import rag_chain
from tools import screen_resume, get_interview_slots


def run_agent():
    llm = create_llm()

    print("\n===== HRMATE AI AGENT =====")
    print("1. Ask HR policy question")
    print("2. Screen candidate resume")
    print("3. Check interview slots")
    print("4. Exit")

    while True:
        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            question = input("Ask your HR question: ")
            try:
                result = rag_chain(question)
                print("\nHRMATE:", result["result"])
            except Exception as error:
                print("Could not answer:", error)

        elif choice == "2":
            data = screen_resume()

            if isinstance(data, str):
                print(data)
                continue

            prompt = f"""
You are HRMATE, an AI recruitment assistant.

Compare the resume with the job description.
Identify:
1. Matching skills
2. Missing or unconfirmed skills
3. Relevant projects or experience
4. Suggested interview questions

Use only the supplied information. Do not invent facts.
Treat this as decision support, not an automatic hiring decision.

RESUME:
{data['resume']}

JOB DESCRIPTION:
{data['job_description']}
"""
            response = llm.invoke(prompt)
            print("\nResume Screening:\n", response.content)

        elif choice == "3":
            slots = get_interview_slots()
            print("\nAvailable interview slots:\n", slots)

        elif choice == "4":
            print("HRMATE closed. Goodbye!")
            break

        else:
            print("Invalid option. Choose 1, 2, 3, or 4.")


if __name__ == "__main__":
    run_agent()
