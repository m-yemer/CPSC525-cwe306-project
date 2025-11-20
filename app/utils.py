
'''
This file is mainly for the CLI implementation
'''
import getpass

def prompt_hidden(prompt_text="Password: "):
    # prompt user for input without echo
    try:
        return getpass.getpass(prompt_text)
    except Exception:
        # fallback
        return input(prompt_text)

def clear_screen():
    # clear terminal
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
