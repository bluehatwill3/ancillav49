import os
import json
import pickle

class DataIngestor:
    """
    Handles unrestricted data ingestion for Holosyn v41.
    Processes URLs, text books, voice files, and memory objects.
    """
    def __init__(self, archive_path="holosyn_v41_scratch/version3"):
        self.archive_path = archive_path
        if not os.path.exists(archive_path):
            os.makedirs(archive_path)

    def ingest_any(self, data, data_type, metadata=None):
        """
        Normalizes any input into the manifold archive.
        data_type: 'url', 'book', 'voice', 'memory'
        """
        # Create a flexible schema without social media constraints
        entity = {
            "type": data_type,
            "content": data,
            "metadata": metadata or {},
            "source": "unrestricted_ingress"
        }
        
        # Save to the archive
        file_count = len(os.listdir(self.archive_path))
        save_path = os.path.join(self.archive_path, f"entity_{file_count}.pkl")
        
        with open(save_path, 'wb') as f:
            pickle.dump(entity, f)
        return f"Ingested {data_type} entity at {save_path}"

# Implementation Example:
# ingestor = DataIngestor()
# ingestor.ingest_any("https://example.com", "url")
# ingestor.ingest_any("Book Content Here", "book")