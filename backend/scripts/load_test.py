"""Sends several /analyze requests at once to a running API and reports throughput and timings.

Run from backend/ with the virtual environment active:
    python scripts/load_test.py https://your-api.onrender.com
    python scripts/load_test.py http://localhost:8000        # local comparison

Every request is a real check, so it is counted in the stats database (the Insights page).
"""

import asyncio
import statistics
import sys
import time

import httpx

LEVELS = [1, 5, 10, 20]  # simultaneous users
ROUNDS = 2  # each user sends this many requests per level
MESSAGES = [
    {"text": "Your account is blocked. Send your PIN and pay the verification fee now.", "source": "sms"},
    {"text": "Hi mum, I lost my phone, this is my new number. Can you send me money today?", "source": "sms"},
    {"text": "Reminder: your dentist appointment is tomorrow at 10:00.", "source": "sms"},
    {"text": "Congratulations! You won 500,000 RWF. Click the link and enter your card details.", "source": "sms"},
]


async def one_user(client: httpx.AsyncClient, url: str, user: int, results: list) -> None:
    for i in range(ROUNDS):
        body = MESSAGES[(user + i) % len(MESSAGES)]
        start = time.perf_counter()
        try:
            response = await client.post(url, json=body)
            results.append((time.perf_counter() - start, response.status_code))
        except httpx.HTTPError as exc:
            results.append((time.perf_counter() - start, type(exc).__name__))


async def run_level(client: httpx.AsyncClient, url: str, users: int) -> dict:
    results: list = []
    start = time.perf_counter()
    await asyncio.gather(*(one_user(client, url, u, results) for u in range(users)))
    wall = time.perf_counter() - start
    ok = sorted(t for t, status in results if status == 200)
    failed = [status for _, status in results if status != 200]
    return {
        "users": users,
        "requests": len(results),
        "ok": len(ok),
        "failed": failed,
        "throughput": len(ok) / wall,
        "median": statistics.median(ok) if ok else float("nan"),
        "p95": ok[max(0, round(0.95 * len(ok)) - 1)] if ok else float("nan"),
        "max": ok[-1] if ok else float("nan"),
        "wall": wall,
    }


async def main(base: str) -> None:
    base = base.rstrip("/")
    async with httpx.AsyncClient(timeout=120, limits=httpx.Limits(max_connections=50)) as client:
        # Render's free plan sleeps when idle; the first call wakes it and is not counted.
        print(f"Waking {base} ...")
        start = time.perf_counter()
        health = await client.get(f"{base}/health")
        print(f"/health {health.status_code} in {time.perf_counter() - start:.1f}s: {health.text}\n")
        await client.post(f"{base}/analyze", json=MESSAGES[0])  # warm-up, not counted

        print(f"{'Users':>5} {'Reqs':>5} {'OK':>4} {'Req/s':>6} {'Median':>7} {'p95':>7} {'Max':>7} {'Total':>7}")
        for users in LEVELS:
            r = await run_level(client, f"{base}/analyze", users)
            print(
                f"{r['users']:>5} {r['requests']:>5} {r['ok']:>4} {r['throughput']:>6.2f} "
                f"{r['median']:>6.2f}s {r['p95']:>6.2f}s {r['max']:>6.2f}s {r['wall']:>6.1f}s"
                + (f"  failures: {r['failed']}" if r["failed"] else "")
            )
            await asyncio.sleep(3)  # let the server settle between levels


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python scripts/load_test.py <API address, e.g. https://your-api.onrender.com>")
    asyncio.run(main(sys.argv[1]))
