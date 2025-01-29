import pandas as pd
import chromadb
import uuid

class Portfolio:
    def __init__(self, file_path="app/resource/my_portfolio.csv"):
        self.file_path = file_path
        try:
            self.data = pd.read_csv(file_path)
        except FileNotFoundError:
            print(f"Error: The file {file_path} was not found.")
            self.data = pd.DataFrame()
        except Exception as e:
            print(f"Error reading the CSV file: {e}")
            self.data = pd.DataFrame()
        
        self.chroma_client = chromadb.PersistentClient(path="vectorstore")  # Ensure the correct path for persistence
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if self.collection.count() == 0:  # Only add data if the collection is empty
            for _, row in self.data.iterrows():
                self.collection.add(
                    documents=[str(row["Techstack"])],  # Ensure it's a list of strings
                    metadatas={"links": row["Links"]},  # Links as metadata
                    ids=[str(uuid.uuid4())]
                )

    def query_links(self, skills):
        results = self.collection.query(query_texts=[skills], n_results=2)
        return results.get('metadatas', [])  # Returns the links metadata

