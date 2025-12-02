from  typing import Optional

def ask_int(
    prompt: str,
    min_val: Optional[int] = None,
    max_val: Optional[int] = None,
    allow_empty: bool = False,
    default: Optional[int] = None,
) -> int:

    while True:
        raw = input(prompt).strip()
        if raw == "":
            if allow_empty and default is not None:
                print(f"No input, using default value: {default}")
                return default
            print("Error: input cannot be empty. Please enter an integer. ")
            continue

        try:
            val = int(raw)
        except ValueError:
            print("Error: please enter an integer.")
            continue

        if (min_val is not None) and (val < min_val):
            print(f"Error: value must be at least {min_val}.")
            continue
        if (max_val is not None) and (val > max_val):
            print(f"Error: value must be at most {max_val}.")
            continue

        return val


def ask_yes_no(prompt: str) -> bool:
    while True:
        ans = input(prompt).strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print("Please answer with 'y' or 'n'.")


def ask_months_to_run(default_months: int = 6) -> int:
    raw = input(
        f"How many months would you like to run the game for? (default {default_months}): "
    ).strip()
    if raw == "":
        print(f"No input, defaulting to {default_months} months.")
        return default_months

    try:
        months = int(raw)
        if months <= 0:
            print(f"Months must be positive. Defaulting to {default_months}.")
            return default_months
        return months
    except ValueError:
        print(f"Invalid input, defaulting to {default_months} months.")
        return default_months
