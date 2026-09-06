import os
import pickle
import uuid

class HolosynIngestor:
    """
    Handles unrestricted data ingestion for Holosyn v41.
    Processes URLs, books, music, voice files, and memory objects.
    """
    def __init__(self, archive_path="holosyn_v41_scratch/version3"):
        self.archive_path = archive_path
        # Ensure the version3 archive exists
        os.makedirs(self.archive_path, exist_ok=True)

    def ingest(self, content, data_type, label=None):
        """
        Normalizes and saves any input object to the manifold archive.
        data_type: 'url', 'book', 'music', 'voice', 'memory'
        """
        # Create a unique ID for the entity to avoid social media dependency
        entity_id = str(uuid.uuid4())
        
        # Build the flexible entity structure
        entity = {
            "id": entity_id,
            "type": data_type,
            "label": label or "unnamed_entity",
            "payload": content  # Can be string, bytes, or any serialized object
        }
        
        # Serialize and save to the archive[cite: 14, 15]
        save_path = os.path.join(self.archive_path, f"{entity_id}.pkl")
        with open(save_path, 'wb') as f:
            pickle.dump(entity, f)
            
        print(f"[Ingestor] Successfully ingested {data_type} as {save_path}")
        return entity_id

# Implementation Example:
# ingestor = HolosynIngestor()
# ingestor.ingest("https://example-book.com", "url", label="My Reading List")
# ingestor.ingest(b"voice_data_bytes", "voice", label="Internal Memory 01")