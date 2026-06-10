import time
import queue
import threading
from concurrent.futures import ThreadPoolExecutor

import dns.message
import dns.query
import dns.rdatatype

DNS_SERVER = "127.0.0.1"
RETRIES = 5
THREADS = 50
QPS = 50  # total queries per second across all workers



OTHER_DOMAINS = [
    "google.com",
    "microsoft.com",
    "example.com"
]

DE_DOMAINS = [
    "amazon.de",
    "sedo.de",
    "google.de",
    "bund.de"
]

DOMAINS = [
    *OTHER_DOMAINS,
    *DE_DOMAINS
] * 50000


work_queue = queue.Queue()


def do_dns_query(domain, timeout=3):
    try:
        query = dns.message.make_query(domain, dns.rdatatype.A, want_dnssec=True)

        response = dns.query.udp(
            query,
            DNS_SERVER,
            timeout=timeout,
        )

        if response.rcode() == dns.rcode.NOERROR:
            return True
        else:
            print(f"Failed {domain}. Retrying.")
            def retry_query():
                try:
                    dns.query.udp(
                        query, DNS_SERVER,
                        timeout=1,
                    )
                except Exception:
                    pass
            for _ in range(RETRIES):
                threading.Thread(
                    target=retry_query, daemon=True
                ).start()
            return False

    except Exception:
        return False


class RateLimiter:
    def __init__(self, qps):
        self.interval = 1.0 / qps
        self.lock = threading.Lock()
        self.next_allowed = time.monotonic()

    def wait(self):
        with self.lock:
            now = time.monotonic()

            if now < self.next_allowed:
                sleep_time = self.next_allowed - now
                time.sleep(sleep_time)

            self.next_allowed = max(
                self.next_allowed + self.interval,
                time.monotonic()
            )


rate_limiter = RateLimiter(QPS)


def schedule_domain(domain, delay=0):
    def delayed_put():
        if delay:
            time.sleep(delay)
        work_queue.put((domain, 0))

    threading.Thread(
        target=delayed_put,
        daemon=True
    ).start()


def worker(worker_id):
    while True:
        domain, retry_count = work_queue.get()

        rate_limiter.wait()

        success = do_dns_query(domain)

        # if success:
        #     print(f"[{worker_id}] OK    {domain}")
        # else:
        #     print(f"[{worker_id}] FAIL  {domain}")

        # Schedule next routine check
        schedule_domain(domain, delay=60)

        work_queue.task_done()


def main():
    for domain in DOMAINS:
        work_queue.put((domain, 0))

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        for worker_id in range(THREADS):
            executor.submit(worker, worker_id)

        while True:
            time.sleep(3600)


if __name__ == "__main__":
    main()