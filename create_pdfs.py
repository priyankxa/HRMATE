
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

documents = {
    "handbook/company_handbook.pdf": {
        "title": "Sample Company Handbook",
        "content": [
            ("Leave Policy", "Employees receive 12 casual leave days per year."),
            ("Working Hours", "Standard working hours are Monday to Friday, 9 AM to 5 PM."),
            ("Benefits", "Eligible full-time employees receive health insurance benefits."),
            ("Remote Work", "Employees may request remote work with manager approval."),
            ("Interview Process", "Candidates attend an initial screening interview followed by a technical interview.")
        ]
    },
    "job_description/ai_developer_jd.pdf": {
        "title": "Junior AI Developer Job Description",
        "content": [
            ("Role", "Junior AI Developer"),
            ("Responsibilities", "Build AI applications, work with language models, and develop document retrieval systems."),
            ("Required Skills", "Python, LangChain, Retrieval-Augmented Generation (RAG), vector databases, and API integration."),
            ("Preferred Skills", "Streamlit, ChromaDB, and Ollama."),
            ("Qualifications", "Basic programming knowledge and willingness to learn AI development.")
        ]
    },
    "resumes/candidate_01.pdf": {
        "title": "Sample Candidate Resume",
        "content": [
            ("Candidate", "Alex Sharma (fictional candidate)"),
            ("Skills", "Python, LangChain, Streamlit, and API integration."),
            ("Projects", "Built a Python chatbot, created a Streamlit dashboard, and developed a basic document question-answering application."),
            ("Experience", "Completed academic projects involving Python programming and AI tools."),
            ("Education", "Computer Science student.")
        ]
    }
}

styles = getSampleStyleSheet()

for relative_path, document in documents.items():
    output_path = DATA_DIR / relative_path
    output_path.parent.mkdir(parents=True, exist_ok=True)

    story = [Paragraph(document["title"], styles["Title"]), Spacer(1, 16)]

    for heading, text in document["content"]:
        story.append(Paragraph(heading, styles["Heading2"]))
        story.append(Paragraph(text, styles["BodyText"]))
        story.append(Spacer(1, 10))

    pdf = SimpleDocTemplate(str(output_path), pagesize=letter)
    pdf.build(story)
    print(f"Created: {output_path.relative_to(BASE_DIR)}")

print("\nAll three sample PDFs created successfully!")
