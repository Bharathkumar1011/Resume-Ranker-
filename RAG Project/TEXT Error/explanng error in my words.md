**Error**:
from langchain.docstore.document import Document as LangchainDocument

RAW_KNOWLEDGE_BASE = [
    LangchainDocument(page_content=doc["text"], metadata={"source": doc["source"]})
    for doc in tqdm(ds)
]

**error name**:text key error

why:
as my knowledge base is of json formt containng structred resumes rathar than bulk of documented text 
there is no key feature of text in our knowldge base 
thats why the error ocuured in firdt place

**how to fix**:

page_content=doc["text"]
above line specifies that all the text in doc is stored as page _content nd this page _Content is what later chuked and converted into vector database
so it must contn all key featuure of knowledge bse otherwise the whole retriver procce swll be nefficient duw to lack of usefull knowlgde
we will creating a infficint RAG project

to avoid that
we need to add all the key feature in our knowlgde base and tereate through whole knowldge base

**corrected code**:
from langchain.docstore.document import Document as LangchainDocument
from tqdm import tqdm

RAW_KNOWLEDGE_BASE = []
for doc in tqdm(ds):
    try:
        # Combine multiple fields for a richer page_content
        page_content = (
            f"Name: {doc.get('name', 'N/A')}. "
            f"Skills: {', '.join(doc.get('skills', []))}. "
            f"Experience: {doc.get('experience', [{}])[0].get('description', 'No experience listed')}. "
            f"Education: {doc.get('education', {}).get('degree', 'No degree listed')}"
        )
        metadata = {"source": "synthetic_resumes.json"}
        RAW_KNOWLEDGE_BASE.append(LangchainDocument(page_content=page_content, metadata=metadata))
    except KeyError as e:
        print(f"Skipping document due to missing key: {e}")



 above code pushes all key feature sinto pge content and creates a fully efficient RW KNOWLGDE BASE

 **Summary**
The text key error occurs because your dataset does not have a "text" key.

Inspect the structure of your dataset (ds) and adjust the code to use the correct keys.
Step 1: Inspect the Structure of ds
Print the first few records of ds to see its structure:

print(ds[0])  # Print the first record

Add error handling to handle missing or nested keys.

Verify the output to ensure the LangchainDocument objects are created correctly.       
for doc in RAW_KNOWLEDGE_BASE[:5]:
    print(doc)

above eexplanaton is the whole of why key error occured and how solve it

