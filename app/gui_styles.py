'''
Modern GUI styles and colors - Shared between both versions
'''

# Modern color scheme
COLORS = {
    'primary': '#2563eb',
    'primary_dark': '#1d4ed8',
    'secondary': '#64748b',
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'light': '#f8fafc',
    'dark': '#1e293b',
    'background': '#ffffff',
    'surface': '#f1f5f9'
}

def setup_styles():
    """Configure modern ttk styles"""
    import tkinter as tk
    from tkinter import ttk
    
    style = ttk.Style()
    style.theme_use('clam')
    
    # Primary button style
    style.configure('Primary.TButton',
                   background=COLORS['primary'],
                   foreground='white',
                   borderwidth=0,
                   focuscolor=COLORS['primary_dark'],
                   padding=(20, 12))
    style.map('Primary.TButton',
              background=[('active', COLORS['primary_dark']),
                         ('pressed', COLORS['primary_dark'])])
    
    # Secondary button style
    style.configure('Secondary.TButton',
                   background=COLORS['secondary'],
                   foreground='white',
                   borderwidth=0,
                   padding=(20, 12))
    style.map('Secondary.TButton',
              background=[('active', '#475569'),
                         ('pressed', '#475569')])
    
    # Danger button style
    style.configure('Danger.TButton',
                   background=COLORS['danger'],
                   foreground='white',
                   borderwidth=0,
                   padding=(20, 12))
    style.map('Danger.TButton',
              background=[('active', '#dc2626'),
                         ('pressed', '#dc2626')])
    
    # Success button style
    style.configure('Success.TButton',
                   background=COLORS['success'],
                   foreground='white',
                   borderwidth=0,
                   padding=(20, 12))
    style.map('Success.TButton',
              background=[('active', '#059669'),
                         ('pressed', '#059669')])

def create_modern_button(parent, text, command, style='Primary.TButton', width=20):
    """Create a modern styled button"""
    from tkinter import ttk
    return ttk.Button(parent, text=text, command=command, style=style, width=width)

def create_modern_frame(parent, padding=10):
    """Create a modern framed container"""
    from tkinter import ttk
    return ttk.Frame(parent, padding=padding)