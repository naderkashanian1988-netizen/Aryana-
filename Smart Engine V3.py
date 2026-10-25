
import random
import time
import os
from datetime import datetime

ACCOUNTS = ["Account 1", "Account 2", "Account 3"]
MAX_USAGE = 3
TOTAL_ACTIONS = 12
DELAY = 0.5

# ذخیره گزارش کنار فایل برنامه
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "engine_v3_log.txt")


def log(message):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{now}] {message}"

    print(line)

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(line + "\n")


def show_previous_log():
    print("\n--- PREVIOUS REPORT ---")

    if not os.path.exists(LOG_FILE):
        print("No previous report found.")
        return

    with open(LOG_FILE, "r", encoding="utf-8") as file:
        lines = file.readlines()

    if not lines:
        print("Previous report is empty.")
    else:
        for line in lines[-10:]:
            print(line.rstrip())

    print("--- END PREVIOUS REPORT ---\n")


def run_engine():
    show_previous_log()

    current_account = 0
    usage_count = 0
    total_usage = {name: 0 for name in ACCOUNTS}
    actions_done = 0

    log("===== NEW SESSION =====")
    log("Smart Engine V3 started")
    log("Mode: SIMULATION ONLY")
    log("No real phone actions will be performed.")

    while actions_done < TOTAL_ACTIONS:
        try:
            account = ACCOUNTS[current_account]
            action = random.choice(["Swipe", "Tap", "Wait"])

            log(f"{account} -> {action}")

            usage_count += 1
            total_usage[account] += 1
            actions_done += 1

            log(
                f"Action {actions_done}/{TOTAL_ACTIONS} | "
                f"Usage: {usage_count}/{MAX_USAGE}"
            )

            time.sleep(DELAY)

            if usage_count >= MAX_USAGE:
                log(f"{account}: test limit reached")
                current_account = (
                    current_account + 1
                ) % len(ACCOUNTS)
                usage_count = 0
                log(f"Next account: {ACCOUNTS[current_account]}")

        except KeyboardInterrupt:
            log("Stopped by user.")
            break

        except Exception as error:
            log(f"ERROR: {error}")
            break

    log("===== FINAL REPORT =====")
    log(f"Actions completed: {actions_done}/{TOTAL_ACTIONS}")

    for name, count in total_usage.items():
        log(f"{name}: {count} simulated actions")

    log(f"Report saved to: {LOG_FILE}")
    log("Simulation finished.")


if __name__ == "__main__":
    run_engine()