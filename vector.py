from langchain.document_loaders import TextLoader, CSVLoader, PyMuPDFLoader, UnstructuredWordDocumentLoader, \
    UnstructuredEPubLoader, UnstructuredMarkdownLoader, UnstructuredODTLoader, EverNoteLoader, UnstructuredHTMLLoader, \
    UnstructuredPowerPointLoader
from langchain.indexes import VectorstoreIndexCreator

# Map file extensions to document loaders and their arguments
LOADER_MAPPING = {
    ".csv": (CSVLoader, {}),
    ".doc": (UnstructuredWordDocumentLoader, {}),
    ".docx": (UnstructuredWordDocumentLoader, {}),
    ".enex": (EverNoteLoader, {}),
    ".epub": (UnstructuredEPubLoader, {}),
    ".html": (UnstructuredHTMLLoader, {}),
    ".md": (UnstructuredMarkdownLoader, {}),
    ".odt": (UnstructuredODTLoader, {}),
    ".pdf": (PyMuPDFLoader, {}),
    ".ppt": (UnstructuredPowerPointLoader, {}),
    ".pptx": (UnstructuredPowerPointLoader, {}),
    ".txt": (TextLoader, {"encoding": "utf8"}),
}


# call the appropriate loader based on the file format
def get_loader(filepath):
    ext = "." + filepath.rsplit(".", 1)[-1]
    if ext in LOADER_MAPPING:
        loader_class, loader_args = LOADER_MAPPING[ext]
        loader = loader_class(filepath, **loader_args)
        return loader

    raise ValueError(f"Unsupported file extension '{ext}'")


def ingest(directory_path):
    loader = get_loader(directory_path)
    index = VectorstoreIndexCreator().from_loaders([loader])

    return index
