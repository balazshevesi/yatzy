def prompt(str: str):
    input_value = input(str)
    match input_value:
        case "exit" | "quit" | "close" | ":q":
            quit()
    return input_value
