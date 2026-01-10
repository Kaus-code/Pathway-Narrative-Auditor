import pathway as pw
import asyncio
from src.auditor import NarrativeAuditor

class MockIndex:
    def query(self, query_table, k=3):
        # Return query_table with an added 'result' column containing dummy context
        # query_table has column 'query'
        return query_table.select(
            query=pw.this.query,
            result=[{"text": "Context info 1"}, {"text": "Context info 2"}]
        )

def test_auditor():
    print("Testing Auditor in isolation...")
    
    # Mock data
    claims_data = ["Claim 1", "Claim 2"]
    import pandas as pd
    claims_df = pd.DataFrame({"claim": ["Claim 1", "Claim 2"]})
    claims_table = pw.debug.table_from_pandas(claims_df)
    
    # Initialize Auditor with mock index
    index = MockIndex()
    # We use a dummy model to avoid API key requirement for this connection test
    # (Though auditor calls litellm, we expect it to fail gracefully or we mock verifying too?)
    # Auditor uses a UDF 'verify_claim'. 
    # To test fully we need it to run. We can mock litellm.acompletion if we want, 
    # but for now let's just see if the Pathway graph builds and runs.
    
    auditor = NarrativeAuditor(index_table=index, llm_config={"model": "mock/model", "api_key": "dummy"})
    
    results = auditor.audit_backstory(claims_table)
    
    # Provide a mock for litellm.acompletion?
    # It's inside a UDF, which runs in a worker. 
    # If we run with 'pw.debug.compute_and_print', it runs locally.
    # We can try to patch litellm in the UDF scope or just let it error/handle it.
    # The UDF has a try/except block.
    
    print("Computing Auditor results...")
    pw.debug.compute_and_print(results)

if __name__ == "__main__":
    test_auditor()
