import pathway as pw
try:
    from pathway.xpacks import llm
    print(f"llm type: {type(llm)}")
    print(f"llm dir: {dir(llm)}")
    if hasattr(llm, 'embedders'):
        print(f"llm.embedders type: {type(llm.embedders)}")
        print(f"llm.embedders dir: {dir(llm.embedders)}")
    if hasattr(llm, 'vector_store'):
        server_cls = llm.vector_store.VectorStoreServer
        import inspect
        try:
            print(f"retrieve_query signature: {inspect.signature(server_cls.retrieve_query)}")
            print(f"retrieve_query doc: {server_cls.retrieve_query.__doc__}")
        except Exception as e:
            print(f"Could not inspect retrieve_query: {e}")

except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Error: {e}")
