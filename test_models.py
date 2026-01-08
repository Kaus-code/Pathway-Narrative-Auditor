import os
import asyncio
from litellm import acompletion
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

async def test_model(model_name):
    print(f"Testing {model_name}...")
    try:
        response = await acompletion(
            model=model_name,
            messages=[{"role": "user", "content": "Hello"}],
            api_key=api_key
        )
        print(f"SUCCESS: {model_name}")
        return True
    except Exception as e:
        print(f"FAILED: {model_name} - {e}")
        return False

async def main():
    models = [
        "gemini/gemini-2.0-flash",
        "gemini/gemini-flash-latest"
    ]
    for m in models:
        if await test_model(m):
            break

if __name__ == "__main__":
    asyncio.run(main())
