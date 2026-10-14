
from pathlib import Path
import json

from pypdf import PdfReader


BASE_DIR = Path(__file__).parent
RESUME_DIR = BASE_DIR / "data" / "resumes"
JOB_DIR = BASE_DIR / "data" / "job_description"

SLOTS_FILE = BASE_DIR / "interview_slots.json"


def extract_pdf_text(pdf_path):
    """Extract text from a PDF file."""
    path = Path(pdf_path)

    if not path.exists():
        return ""

    reader = PdfReader(str(path))
    return "\n".join(
        page.extract_text() or ""
        for page in reader.pages
    )


def screen_resume(resume_filename="candidate_01.pdf"):
    """Compare a candidate resume with the AI developer job description."""
    resume_path = RESUME_DIR / resume_filename
    job_path = JOB_DIR / "ai_developer_jd.pdf"

    resume_text = extract_pdf_text(resume_path)
    job_text = extract_pdf_text(job_path)

    if not resume_text:
        return "Resume not found or no readable text in the PDF."

    if not job_text:
        return "Job description not found or no readable text in the PDF."

    return {
        "resume": resume_text,
        "job_description": job_text,
        "instruction": (
            "Compare the resume with the job description. "
            "Identify matching skills, missing requirements, "
            "relevant experience, and questions to clarify. "
            "Use evidence from the documents and do not invent details."
        )
    }


def get_interview_slots():
    """Return available interview slots from the mock calendar."""
    if not SLOTS_FILE.exists():
        return "Interview calendar not found. Create interview_slots.json first."

    with open(SLOTS_FILE, "r", encoding="utf-8") as file:
        slots = json.load(file)

    available = [
        slot for slot in slots
        if slot.get("available", False)
    ]

    if not available:
        return "No interview slots are currently marked available."

    return available


if __name__ == "__main__":
    print("HRMATE Tools Test")
    print("\n1. Resume screening data")
    print(screen_resume())

    print("\n2. Interview slots")
    print(get_interview_slots())
