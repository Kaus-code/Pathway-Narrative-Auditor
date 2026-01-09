"""
Module: auditor.py
Description: The reasoning agent that validates claims against the index.
"""

import pandas as pd
import pathway as pw

class NarrativeAuditor:
    """
    Audits claims by querying the Pathway index and checking for contradictions.
    """

    def __init__(self, index_table: pw.Table, llm_config: dict = None):
        """
        Initialize the auditor.

        Args:
            index_table (pw.Table): The Pathway table serving as the vector index.
            llm_config (dict): Configuration for the reasoning engine (LiteLLM/OpenAI).
        """
        self.index_table = index_table
        self.llm_config = llm_config

    async def audit_claim(self, claim: str) -> dict:
        """
        Verifies a single claim against the context.
        """
        # Rate Limiting for Free Tier
        import asyncio
        await asyncio.sleep(15)

        # 1. Retrieve Context
        # We need to construct a query table for this specific claim
        # Since this is running inside a UDF (conceptually), we assume we can query the index.
        # However, Pathway UDFs cannot easily query the index directly if it's a separate stream.
        # DESIGN CHANGE: The Auditor should receive the context from the retrieval step.
        # For this hackathon implementation, we simplified: Auditor has access to valid index query.
        
        # We use the retrieve_query logic wrapper or direct call if possible.
        # Since we are inside a coroutine, we can try to call the server.
        
        # For now, let's assume we can query.
        pass

    def audit_backstory(self, claims_table: pw.Table) -> pw.Table:
        """
        Audits a table of claims against the vector index.

        Args:
            claims_table (pw.Table): Table containing 'claim' column.

        Returns:
            pw.Table: Table with 'claim', 'context', and 'verification_result'.
        """
        # 1. Retrieve context for each claim from the index
        # We assume self.index_table is a Pathway VectorStore definition (contextualized table)
        # or we use knn matching.
        # If self.index_table is the result of llm.vector_store, it's a VectorStoreServer.
        # We can use the 'query' method which returns the table with added context.
        
        # Check if index has .retrieve_query method (standard xpack)
        if hasattr(self.index_table, "retrieve_query"):
             # Perform RAG retrieval
             # retrieve_query expects specific schema: query, k, filepath_globpattern, metadata_filter
             query_table = claims_table.select(
                 query=pw.this.claim,
                 k=3,
                 filepath_globpattern="*", # Match all
                 metadata_filter=None # No filter
             )
             enriched_claims = self.index_table.retrieve_query(query_table)
        elif hasattr(self.index_table, "query"):
             enriched_claims = self.index_table.query(claims_table.select(query=pw.this.claim), k=3)
        else:
             raise ValueError("Index does not support query interface.")

        # enriched_claims now has 'query' (the claim) and 'result' (list of chunks/docs)
        
        # 2. Verify consistency using LLM
        @pw.udf
        async def verify_claim(claim: str, context: list[dict]) -> dict:
            import asyncio
            await asyncio.sleep(15)
            prompt = f"Claim: {claim}\\nContext: {context}\\nIs this claim consistent with the context? Return JSON {{'consistent': bool, 'reason': str}}"
            # Simplified LLM call
            from litellm import acompletion
            import json
            try:
                resp = await acompletion(
                    model=self.llm_config.get("model", "gemini/gemini-flash-latest"),
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"},
                    api_key=self.llm_config.get("api_key")
                )
                return json.loads(resp.choices[0].message.content)
            except Exception:
                return {"consistent": False, "reason": "Error during verification"}

        results = enriched_claims.select(
            claim=claims_table.claim,
            context=pw.this.result,
            verification=verify_claim(claims_table.claim, pw.this.result)
        )
        
        return results
