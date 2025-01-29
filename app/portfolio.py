import pandas as pd
import chromadb
import uuid
import os

class Portfolio:
    def __init__(self, file_path="app/resource/my_portfolio.csv"):
        self.file_path = file_path
        
        # Ensure vectorstore directory exists
        os.makedirs("vectorstore", exist_ok=True)
        
        try:
            self.data = pd.read_csv(file_path)
        except FileNotFoundError:
            print(f"Error: The file {file_path} was not found.")
            self.data = pd.DataFrame()
        except Exception as e:
            print(f"Error reading the CSV file: {e}")
            self.data = pd.DataFrame()
        
        # Initialize ChromaDB with new client configuration
        self.chroma_client = chromadb.Client(
            chromadb.HttpClient(
                host="localhost",
                port=8000
            )
        )

        # Create or get collection
        try:
            self.collection = self.chroma_client.get_collection(name="portfolio")
        except:
            self.collection = self.chroma_client.create_collection(name="portfolio")

    def load_portfolio(self):
        if not self.data.empty:
            for _, row in self.data.iterrows():
                try:
                    # Convert techstack to string if it's not already
                    techstack = str(row["Techstack"]) if not isinstance(row["Techstack"], str) else row["Techstack"]
                    
                    self.collection.add(
                        documents=[techstack],
                        metadatas=[{"links": str(row["Links"])}],
                        ids=[str(uuid.uuid4())]
                    )
                except Exception as e:
                    print(f"Error adding document: {e}")

    def query_links(self, skills):
        try:
            if isinstance(skills, list):
                query_text = " ".join(skills)
            else:
                query_text = str(skills)
                
            results = self.collection.query(
                query_texts=[query_text],
                n_results=2
            )
            return results.get('metadatas', [])
        except Exception as e:
            print(f"Error querying links: {e}")
            return []
