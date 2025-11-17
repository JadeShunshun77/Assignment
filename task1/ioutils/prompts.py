def ask_positive_int(prompt: str, allow_zero: bool = False) -> int:
    """
    要求用户输入一个正整数（或者允许 0）。
    处理空输入和非数字输入。
    """
    while True:
        raw = input(prompt).strip()
        if not raw:
            print("No input, please enter a number.")
            continue
        if not raw.lstrip("-").isdigit():
            print("Invalid input, please enter an integer.")
            continue

        val = int(raw)
        if allow_zero and val == 0:
            return val
        if val <= 0:
            print("Please enter a positive integer.")
            continue
        return val
