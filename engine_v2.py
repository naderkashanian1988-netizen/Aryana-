
import random
import time
import traceback
from datetime import datetime

# تنظیمات موتور
ACCOUNTS = ["Account 1", "Account 2", "Account 3"]
MAX_USAGE = 3
TOTAL_ACTIONS = 12
DELAY = 0.5

def log(message):
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] {message}")

def run_engine():
    current_account = 0
    usage_count = 0
    total_usage = {name: 0 for name in ACCOUNTS}
    actions_done = 0

    log("Smart Engine V2 started")
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
                f"Account usage: {usage_count}/{MAX_USAGE}"
            )

            time.sleep(DELAY)

            if usage_count >= MAX_USAGE:
                log(f"{account}: test limit reached")
                current_account = (current_account + 1) % len(ACCOUNTS)
                usage_count = 0
                log(f"Next account: {ACCOUNTS[current_account]}")

        except KeyboardInterrupt:
            log("Stopped by user.")
            break

        except Exception as error:
            log(f"Error: {error}")
            traceback.print_exc()
            break

    log("----- FINAL REPORT -----")
    log(f"Actions completed: {actions_done}/{TOTAL_ACTIONS}")

    for name, count in total_usage.items():
        log(f"{name}: {count} simulated actions")

    log("Simulation finished.")

if __name__ == "__main__":
    run_engine()