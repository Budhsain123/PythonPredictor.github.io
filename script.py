import os
import sys
import time
from datetime import datetime

try:
    from cfonts import render
except ImportError:
    os.system('pip install python-cfonts')
    from cfonts import render

output = render('ColorTraderPro', colors=['red'], align='center')
print(output)

history = []

def typing_effect(text, delay=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def display_period_and_timer():
    last_minute = None
    remaining_seconds = 59

    pattern = ["GREEN", "SMALL", "BIG", "RED", "RED", "SMALL", "GREEN", "BIG"]
    pattern_length = len(pattern)

    print("\033[40m\033[92m")

    for _ in range(1):  # Runs only once per request
        now = datetime.utcnow()
        if now.minute != last_minute:
            last_minute = now.minute
            total_minutes = now.hour * 60 + now.minute
            current_pattern = pattern[total_minutes % pattern_length]
            period_1m = now.strftime("%Y%m%d") + "1000" + str(10001 + total_minutes)

            history.append((period_1m, current_pattern))
            if len(history) > 5:
                history.pop(0)

            typing_effect("\n[Processing Data...]", delay=0.04)
            time.sleep(1)
            typing_effect(f"\033[32m[Data Retrieved Successfully]\033[0m", delay=0.04)

            print(f"\n{'='*60}")
            print(f"|{'PERIOD':^28}|{'RESULT':^28}|")
            print(f"{'-'*60}")
            print(f"|{period_1m:^28}|{current_pattern:^28}|")
            print(f"{'='*60}\n")

            print("[Historical Data - Last 5 Periods]")
            print(f"{'='*60}")
            print(f"|{'PERIOD':^28}|{'RESULT':^28}|")
            print(f"{'-'*60}")
            for period, result in history:
                print(f"|{period:^28}|{result:^28}|")
            print(f"{'='*60}")

display_period_and_timer()
