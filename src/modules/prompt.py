def prompt(str: str):
    input_value = input(str)
    if input_value == "exit" or input_value == "quit":
        quit()
    return input_value
