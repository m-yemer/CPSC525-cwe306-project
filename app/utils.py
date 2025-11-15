

import getpass

def prompt_hidden(prompt_text="Password: "):
    try:
        return getpass.getpass(prompt_text)
    except Exception:
        # fallback
        return input(prompt_text)

def clear_screen():
    # Besteffort clear for many terminals
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
