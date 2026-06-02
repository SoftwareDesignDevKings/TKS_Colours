import asyncio
import sys
import os

# Add backend directory to sys.path to resolve seed_data
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from seed_data import seed

if __name__ == "__main__":
    asyncio.run(seed())
