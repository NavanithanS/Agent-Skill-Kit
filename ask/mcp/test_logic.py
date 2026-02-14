import asyncio
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from ask.mcp.server import list_skills, search_skills, get_skill

async def main():
    print("--- Testing list_skills ---")
    skills = await list_skills()
    print(skills)
    
    print("\n--- Testing search_skills('security') ---")
    search = await search_skills("security")
    print(search)
    
    if "No skills found" in skills:
        print("\n❌ Logic Error: expected to find skills.")
        sys.exit(1)
        
    print("\n✅ Server Logic Verified.")

if __name__ == "__main__":
    asyncio.run(main())
