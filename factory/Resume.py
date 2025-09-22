from factory.managers import get_real_dir

class Resume:
    def __init__(self, file_path):
        self.file_path = get_real_dir(file_path)
        self.text = self._extract_text()
        self.skills = self._extract_skills()
        self.experience = self._extract_experience()
        self.education = self._extract_education()

    def _extract_text(self):
        # detect file type
        if self.file_path.endswith('.pdf'):
            return self._extract_text_pdf()
        elif self.file_path.endswith('.docx'):
            return self._extract_text_docx()
        else:
            raise ValueError("Unsupported file type")

    def _extract_text_pdf(self):
        import pdfplumber
        text = ""
        with pdfplumber.open(self.file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text

    def _extract_text_docx(self):
        from docx import Document
        doc = Document(self.file_path)
        return "\n".join([p.text for p in doc.paragraphs])

    def _extract_skills(self):
        # Basic keyword search or NLP
        keywords = ["Python", "Java", "SQL", "AWS", "Django", "FastAPI"]
        found = [k for k in keywords if k.lower() in self.text.lower()]
        return found

    def _extract_experience(self):
        # Implement regex or NLP to find years of experience
        return []

    def _extract_education(self):
        # Parse degrees / schools
        return []
