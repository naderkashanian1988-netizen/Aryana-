
import os
import re
import time
from datetime import datetime

ACCOUNTS = ["Account 1", "Account 2", "Account 3"]
MAX_USAGE = 3
DELAY = 0.3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "engine_v4_log.txt")

# پیام‌های آزمایشی؛ عمداً شامل حالت‌های مختلف هستند
TEST_MESSAGES = [
    ("Welcome", False),
    ("Limit Reached", True),
    ("Everything is working", False),
    ("limit reached", True),
    ("You have reached your usage limit", True),
    ("Temporary error", False),
    ("LIMIT REACHED!", True),
    ("Try again later", False),
]


def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    print(line)

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(line + "\n")


def detect_limit(message):
    """تشخیص چند شکل رایج پیام محدودیت"""
    text = re.sub(r"\s+", " ", message.lower()).strip()

    patterns = [
        r"\blimit\s+reached\b",
        r"\breached\s+your\s+(?:usage\s+)?limit\b",
        r"\busage\s+limit\s+exceeded\b",
    ]

    return any(re.search(pattern, text) for pattern in patterns)


def test_detector():
    log("===== DETECTOR TESTS =====")
    passed = 0

    for message, expected in TEST_MESSAGES:
        result = detect_limit(message)
        success = result == expected

        if success:
            passed += 1

        log(
            f"Message: {message!r} | "
            f"Expected: {expected} | "
            f"Detected: {result} | "
            f"{'PASS' if success else 'FAIL'}"
        )

    log(f"Detector tests: {passed}/{len(TEST_MESSAGES)} passed")
    return passed == len(TEST_MESSAGES)


def simulate_engine():
    log("===== ENGINE SIMULATION =====")
    log("Mode: SIMULATION ONLY")
    log("No real accounts or phone actions.")

    account_index = 0
    usage_count = 0
    account_counts = {name: 0 for name in ACCOUNTS}
    switches = 0

    for number, (message, expected) in enumerate(TEST_MESSAGES, start=1):
        account = ACCOUNTS[account_index]

        log(f"Test {number}: active account = {account}")
        log(f"Received message: {message!r}")

        # بررسی می‌کنیم موتور پیام را درست تشخیص می‌دهد یا نه
        limit_found = detect_limit(message)

        if limit_found:
            log(f"LIMIT DETECTED for {account}")
            log("Switching to next account.")

            account_index = (account_index + 1) % len(ACCOUNTS)
            usage_count = 0
            switches += 1

            log(f"Active account is now {ACCOUNTS[account_index]}")
        else:
            usage_count += 1
            account_counts[account] += 1
            log(f"No limit detected. Usage: {usage_count}/{MAX_USAGE}")

            if usage_count >= MAX_USAGE:
                log(f"Simulated usage cap reached for {account}")
                account_index = (account_index + 1) % len(ACCOUNTS)
                usage_count = 0
                switches += 1
                log(f"Active account is now {ACCOUNTS[account_index]}")

        time.sleep(DELAY)

    log("===== SIMULATION REPORT =====")
    log(f"Messages processed: {len(TEST_MESSAGES)}")
    log(f"Account switches: {switches}")

    for name, count in account_counts.items():
        log(f"{name}: {count} non-limit messages handled")

    log(f"Report file: {LOG_FILE}")


def main():
    log("========== SMART ENGINE V4 ==========")

    detector_ok = test_detector()

    if detector_ok:
        log("Detector result: ALL TESTS PASSED")
    else:
        log("Detector result: SOME TESTS FAILED")

    simulate_engine()
    log("Program finished.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("Program stopped by user.")
    except Exception as error:
        log(f"UNEXPECTED ERROR: {error}")
        raise