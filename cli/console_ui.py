


WIDTH = 90
INNER_WIDTH = WIDTH - 2

def border() -> str:
    pattern = "<>"
    middle = (pattern * WIDTH)[:WIDTH - 2]
    return f"*{middle}*"

def centered(text: str = "") -> str:
    return f"|{text:^{INNER_WIDTH}}|"

def show_header(title: str) -> None:
    print(border())
    print(centered())
    print(centered(title))
    print(centered())

def centered_input(prompt: str) -> str:
    prompt = f"{prompt}: "
    padding = (INNER_WIDTH - len(prompt)) // 2
    return input(
        "|" + " " * padding + prompt
    ).strip()

