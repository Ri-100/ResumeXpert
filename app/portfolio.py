import pandas as pd
import chromadb
import uuid
import shutil
import os

class Portfolio:
    def __init__(self, file_path="app/resource/my_portfolio.csv"):
        self.file_path = file_path
        
        # Clean up existing vectorstore if exists
        if os.path.exists("vectorstore"):
            shutil.rmtree("vectorstore")
        
        try:
            self.data = pd.read_csv(file_path)
        except FileNotFoundError:
            print(f"Error: The file {file_path} was not found.")
            self.data = pd.DataFrame()
        except Exception as e:
            print(f"Error reading the CSV file: {e}")
            self.data = pd.DataFrame()
        
        # Initialize ChromaDB with a clean database
        self.chroma_client = chromadb.PersistentClient(path="vectorstore")
        self.collection = self.chroma_client.create_collection(name="portfolio")

    def load_portfolio(self):
        # Clear existing data
        try:
            self.collection.delete(where={})
        except:
            pass
            
        # Load new data
        for _, row in self.data.iterrows():
            try:
                self.collection.add(
                    documents=[str(row["Techstack"])],
                    metadatas=[{"links": row["Links"]}],  # Ensure metadatas is a list of dicts
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
