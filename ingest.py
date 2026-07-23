import os
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

        return text
    
def load_documents(folder_path):
    documents = []

    for file in os.listdir(folder_path):

        if file.endswith(".pdf"):

            path = os.path.join(folder_path,file)

            text = extract_text_from_pdf(path)

            documents.append({
                "file_name" : file,
                "text" : text
            })

            return documents
        

# if __name__ == "__main__":
#     docs = load_documents("data")
#     for doc in docs:
#         print("="*50)
#         print(doc["file_name"])
#         print(doc['text'][:500])


def chunk_text(text, chunk_size=500 , overlap=100):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def create_chunks(documents):

    all_chunks = []

    for doc in documents:

        chunks = chunk_text(doc["text"])

        for chunk in chunks:

            all_chunks.append({
                "file_name" : doc['file_name'],
                "text" : chunk
            })

    return all_chunks


if __name__ == "__main__":
    docs = load_documents("data")

    chunks = create_chunks(docs)

    print("Total Chunks :" , len(chunks))

    print()

    print(chunks[0]["text"])


