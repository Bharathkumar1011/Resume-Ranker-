import datasets

ds = datasets.load_dataset("m-ric/huggingface_doc", split="train")
Above is the actual step to load the knowledgebase but since  saved my knowledge base as .json file the
code must be altered 
Altered code:
*from datasets import load_dataset*
# Load the JSON file as a dataset
ds = load_dataset("json", data_files="/kaggle/input/knowledge-base/synthetic_resumes.json", split="train")

# Now you can work with the dataset
print(ds[0])  # Access the first record

##both are same but in our project we load the knowlwdge base from memory rather than datasets itself

##
The load_dataset function is versatile and can handle both remote datasets (from the Hub) and local files (like JSON).

##
3. Loading the Knowledge Base from Memory
In your project, you are generating the knowledge base (synthetic resumes) in memory and saving it as a JSON file. Instead of loading the dataset from Hugging Face's Hub, you are loading it from your local JSON file. This is a valid approach because:

Flexibility: You can create and customize your own dataset without relying on pre-existing datasets.

Control: You have full control over the structure and content of the dataset.

Efficiency: If the dataset is small or medium-sized, loading it from memory or a local file is faster than downloading it from a remote source.
