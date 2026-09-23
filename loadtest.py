import asyncio
import aiohttp
import time
from collections import Counter

URL = "http://ad9146c2fce624e8489c9ed7f5503b80-201424773.eu-west-1.elb.amazonaws.com:8000/shirts/get"   # target URL
REQUESTS_PER_SECOND = 300
DURATION_SECONDS = 10
MAX_CONCURRENCY = 500

semaphore = asyncio.Semaphore(MAX_CONCURRENCY)

async def fetch(session):
    async with semaphore:
        try:
            async with session.get(
                URL,
                timeout=aiohttp.ClientTimeout(total=5)
            ) as resp:
                await resp.read()
                # treat 2xx / 3xx as success
                if 200 <= resp.status < 400:
                    return "success"
                else:
                    return "failed"
        except Exception:
            return "failed"

async def rate_limited_requests():
    stats = Counter()

    async with aiohttp.ClientSession() as session:
        start = time.time()
        total_sent = 0

        while time.time() - start < DURATION_SECONDS:
            batch_start = time.time()

            tasks = [
                asyncio.create_task(fetch(session))
                for _ in range(REQUESTS_PER_SECOND)
            ]

            results = await asyncio.gather(*tasks)
            stats.update(results)

            total_sent += len(tasks)

            elapsed = time.time() - batch_start
            await asyncio.sleep(max(0, 1 - elapsed))

    print("\n=== Load Test Results ===")
    print(f"Target URL: {URL}")
    print(f"Duration: {DURATION_SECONDS}s")
    print(f"Total requests sent: {total_sent}")
    print(f"Successful responses: {stats['success']}")
    print(f"Failed responses: {stats['failed']}")
    print(f"Average RPS: {total_sent / DURATION_SECONDS:.1f}")

if __name__ == "__main__":
    asyncio.run(rate_limited_requests())