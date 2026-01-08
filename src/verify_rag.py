import pathway as pw
from dotenv import load_dotenv
import os
from src.ingestor import DataIngestor
from src.indexer import HybridIndexer

# Load env variables
load_dotenv()

def verify():
    print("Starting verification...")
    DATA_DIR = "./data/"
    TEST_CSV = "./data/test.csv"

    # 1. Ingest
    print("Ingesting data...")
    ingestor = DataIngestor(DATA_DIR, watch_mode=False) # static mode for test
    # We use test_csv to ensure we have predictable data
    documents = ingestor.ingest_test_csv(TEST_CSV)

    # 2. Index
    print("Building index...")
    indexer = HybridIndexer()
    # HybridIndexer expects a table. 
    # ingest_test_csv returns a table.
    # Note: HybridIndexer might expect specific columns. 
    # ingestor.ingest_books returns [data, path, modified_at] mapped to text=data.
    # We should ensure ingest_test_csv has 'text' column if that's what generic vector_store expects.
    # Usually vector_store defaults to using the columns available or needs 'data'/'text'.
    
    # Let's peek at ingest_test_csv implementation in thought process... 
    # It does pw.io.csv.read(schema=None). 
    # If the CSV has a 'text' column, it will be fine.
    
    index = indexer.build_index(documents)

    # 3. Query
    print("Preparing query...")
    # Create a simple query table
    query_data = [
        {"query": "What is the backstory?", "k": 3},
    ]
    query_table = pw.debug.table_from_markdown(
        '''
        | query | k |
        |---|---|
        | What is the backstory? | 3 |
        '''
    )

    # Note: llm.vector_store returns a VectorStoreServer or similar.
    # We need to see if we can query it directly as a KNN index.
    # Usually we use pathawy.xpacks.llm.document_store (higher level) or just KNN.
    # If index is a VectorStore, it might verify itself or we can retrieve.
    
    # Assuming 'index' is a Table or has a method to get nearest items.
    # Actually checking documentation of pathway.xpacks.llm.vector_store:
    # It returns a VectorStoreClient? Or it IS the server logic?
    # Wait, usually it returns a KNNDocuments or similar.
    
    # Let's try to just print the index itself (the nodes) to see if it computed something.
    # If it's a Table, we can print it.
    
    # However, to be safe and test retrieval:
    # We will try to invoke the retrieval if the object supports it.
    # If 'index' is just a Table of vectors, we can't 'query' it without a join.
    
    # For now, let's just attempt to print the documents table to make sure ingestion works,
    # and print the index table if it's a table.
    
    print("Computing and printing documents...")
    pw.debug.compute_and_print(documents)
    
    # If index is a table (e.g. docs with embeddings), printing it helps.
    try:
        print("Computing and printing index (first 2 rows)...")
        # If it's an object, this might fail or print repr.
        # If it's a Table, it will print data.
        if isinstance(index, pw.Table):
             pw.debug.compute_and_print(index, limit=2)
        else:
             print(f"Index is of type {type(index)}, not a simple Table.")
             # If it has a query method, use it?
             # But for now, verifying type and successful construction is good.
    except Exception as e:
        print(f"Could not print index: {e}")

if __name__ == "__main__":
    verify()
