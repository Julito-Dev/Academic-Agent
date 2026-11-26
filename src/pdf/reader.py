from pypdf import PdfReader


def read_pdf(route: str) -> str:
    document = PdfReader(route)
    
    text = ""
    
    for page in document:
        text += page.get_text()
    
    document.close()   

    return text