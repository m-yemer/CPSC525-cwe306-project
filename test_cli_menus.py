import sys
import io
from unittest.mock import patch



def run_script(module_name, input_sequence):
    """Run a CLI module with a sequence of inputs, capturing output."""
    import importlib
    mod = importlib.import_module(module_name)
    inputs = iter(input_sequence)
    output = io.StringIO()
    def next_input(prompt=None):
        return next(inputs)
    with patch('builtins.input', next_input), patch('getpass.getpass', next_input), patch('sys.stdout', output):
        try:
            mod.main_loop()
        except StopIteration:
            pass  # End of input sequence
    return output.getvalue()

def test_main_fix():
    # login as alice, go to admin tools, back, user menu, back, quit
    inputs = [
        '1',        # login
        'alice',    # username
        'alicepw',  # password
        '3',        # admin tools
        '3',        # back from admin tools
        '4',        # use app (user menu)
        '7',        # back to main menu
        '5'         # quit
    ]
    out = run_script('app.main_fix', inputs)
    print('--- main_fix.py output ---')
    print(out)

def test_main_vuln():
    # login as alice, go to admin tools, back, user menu, back, quit
    inputs = [
        '1',        # login
        'alice',    # username
        'alicepw',  # password
        '3',        # admin tools
        '3',        # back from admin tools
        '4',        # use app (user menu)
        '7',        # back to main menu
        '5'         # quit
    ]
    out = run_script('app.main_vuln', inputs)
    print('--- main_vuln.py output ---')
    print(out)

if __name__ == '__main__':
    print('Testing main_fix.py...')
    test_main_fix()
    print('\nTesting main_vuln.py...')
    test_main_vuln()
    print('\nAll CLI menu tests completed successfully!')
