from qdrant_client import models, QdrantClient
from ..VectorDBInterface import VectorDBInterface
from ..VectorDBEnums import DistanceMethodEnums
import logging
from typing import List


class QdrantDBProvider(VectorDBInterface):

    def __init__(self, db_path: str, distance_method: str):
        self.db_path = db_path
        self.distance_method = None
        self.client = None

        if distance_method == DistanceMethodEnums.COSINE.value:
            self.distance_method = models.Distance.COSINE
        elif distance_method == DistanceMethodEnums.DOT.value:
            self.distance_method = models.Distance.DOT

        self.logger = logging.getLogger(__name__)

    def connect(self):
        self.client = QdrantClient(path=self.db_path)

    def disconnect(self):
        self.client = None

    def is_collection_existed(self, collection_name: str) -> bool:
        return self.client.collection_exists(collection_name=collection_name)

    def list_all_collections(self):
        return self.client.get_collections()

    def get_collection_info(self, collection_name: str) -> dict:
        return self.client.get_collection(collection_name=collection_name)

    def delete_collection(self, collection_name: str):
        if self.is_collection_existed(collection_name):
            return self.client.delete_collection(collection_name=collection_name)

    def create_collection(
        self, collection_name: str, embedding_size: int, do_reset=False
    ):
        if do_reset:
            _ = self.delete_collection(collection_name)

        if not self.is_collection_existed(collection_name=collection_name):
            _ = self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=embedding_size,
                    distance=self.distance_method,
                ),
            )
            return True
        else:
            # Check if the existing collection has the correct size
            collection_info = self.client.get_collection(collection_name=collection_name)
            
            # Extract current size depending on how vectors are configured
            current_size = 0
            if hasattr(collection_info.config.params.vectors, 'size'):
                current_size = collection_info.config.params.vectors.size
            elif isinstance(collection_info.config.params.vectors, dict) and "" in collection_info.config.params.vectors:
                current_size = collection_info.config.params.vectors[""].size
            
            if current_size > 0 and current_size != embedding_size:
                self.logger.warning(
                    f"Collection '{collection_name}' has size {current_size} but expected {embedding_size}. Recreating."
                )
                self.delete_collection(collection_name)
                self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=models.VectorParams(
                        size=embedding_size,
                        distance=self.distance_method,
                    ),
                )
                return True

        return False

    def insert_one(
        self,
        collection_name: str,
        text: str,
        vector: list,
        metadata: dict = None,
        record_id: str = None,
    ):
        if not self.is_collection_existed(collection_name):
            self.logger.error(
                f"cannot insert new record to non-existing collection: {collection_name}"
            )
            return False

        # If no ID provided, you can use a random UUID or pass an integer
        if record_id is None:
            import uuid

            record_id = str(uuid.uuid4())

        self.client.upload_points(
            collection_name=collection_name,
            points=[
                models.PointStruct(
                    id=record_id,  # Must be a string (UUID) or integer, not a list
                    vector=vector,
                    payload={
                        "text": text,
                        "metadata": metadata,
                    },
                )
            ],
        )
        return True

    def insert_many(
        self,
        collection_name: str,
        texts: List[str],
        vectors: List[list],
        metadatas: List[dict] = None,
        record_ids: List[str] = None,
        batch_size: int = 50,
    ):
        if not self.is_collection_existed(collection_name):
            self.logger.error(
                f"cannot insert new record to non-existing collection: {collection_name}"
            )
            return False

        if metadatas is None:
            metadatas = [None] * len(texts)

        if record_ids is None:
            record_ids = list(range(0, len(texts)))

        for i in range(0, len(texts), batch_size):
            batch_end = i + batch_size
            batch_texts = texts[i:batch_end]
            batch_vectors = vectors[i:batch_end]
            batch_metadatas = metadatas[i:batch_end]
            batch_record_ids = record_ids[i:batch_end]

            # Use models.PointStruct instead of models.Record
            batch_points = [
                models.PointStruct(
                    id=batch_record_ids[j],
                    vector=batch_vectors[j],
                    payload={
                        "text": batch_texts[j],
                        "metadata": batch_metadatas[j],
                    },
                )
                for j in range(len(batch_texts))
            ]

            # Indented correctly inside the loop
            try:
                self.client.upload_points(
                    collection_name=collection_name,
                    points=batch_points,  # Changed parameter name to points
                )
            except Exception as e:
                self.logger.error(f"error while inserting batch {e}")
                return False

        return True

    def search_by_vector(self, collection_name: str, vector: list, limit: int = 5):
        response = self.client.query_points(
            collection_name=collection_name,
            query=vector,
            limit=limit,
        )
        return response.points
