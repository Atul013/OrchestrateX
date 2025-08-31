import asyncio
from advanced_client import MultiModelOrchestrator

async def test():
    async with MultiModelOrchestrator() as orch:
        result = await orch.orchestrate_with_critiques('Hello')
        print('Success:', type(result))
        print('Result:', result.__dict__)
        return result

if __name__ == "__main__":
    asyncio.run(test())
