"""
Module: indexer.py
Description: Manages vector indexing using Pathway's LLM XPack.
"""

import pathway as pw
from pathway.xpacks import llm

class HybridIndexer:
    """
    Builds and manages a Hybrid Vector Store (Vector + Keyword) for efficient retrieval.
    """

    def __init__(self, embedder_config: dict = None):
        """
        Initialize the indexer.

        Args:
            embedder_config (dict): Configuration for the embedding model (e.g., LiteLLM/OpenAI).
        """
        self.embedder_config = embedder_config

    def build_index(self, table: pw.Table) -> pw.Table:
        """
        Create a vector index from the ingested text table.

        Args:
            table (pw.Table): Input Pathway table containing text chunks from novels.

        Returns:
            pw.Table: An indexed table ready for ANN search.
        """
        # Create the embedder instance
        embedder = llm.embedders.LiteLLMEmbedder(
            model=self.embedder_config.get("model", "gemini/text-embedding-004"),
            api_key=self.embedder_config.get("api_key")
        )

        # Create a vector store using Pathway's LLM XPack
        # Using VectorStoreServer class from the module
        return llm.vector_store.VectorStoreServer(
            table,
            embedder=embedder,
        )
