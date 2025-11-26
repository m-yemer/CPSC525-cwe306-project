'''
Professional GUI styles and theme configuration
'''

# Professional color palette
COLORS = {
    'primary': '#2c5aa0',
    'primary_dark': '#1e3d72',
    'primary_light': '#4a7bc8',
    'secondary': '#6c757d',
    'success': '#28a745',
    'warning': '#ffc107', 
    'danger': '#dc3545',
    'light': '#f8f9fa',
    'dark': '#343a40',
    'background': '#ffffff',
    'surface': '#f8f9fa',
    'border': '#dee2e6',
    'text_primary': '#212529',
    'text_secondary': '#6c757d'
}

# Professional fonts
FONTS = {
    'title': ('Arial', 16, 'bold'),
    'header': ('Arial', 12, 'bold'),
    'subtitle': ('Arial', 11),
    'body': ('Arial', 10),
    'small': ('Arial', 9)
}

def setup_styles():
    """Configure professional ttk styles"""
    import tkinter as tk
    from tkinter import ttk
    
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configure root background
    style.configure('.', background=COLORS['background'])
    
    # Frame styles
    style.configure('TFrame', background=COLORS['background'])
    style.configure('Card.TFrame', background=COLORS['surface'], relief='raised', borderwidth=1)
    style.configure('Border.TFrame', background=COLORS['background'], relief='solid', borderwidth=1)
    
    # Label styles
    style.configure('TLabel', background=COLORS['background'], font=FONTS['body'])
    style.configure('Title.TLabel', font=FONTS['title'], foreground=COLORS['primary'])
    style.configure('Header.TLabel', font=FONTS['header'], foreground=COLORS['text_primary'])
    style.configure('Subtitle.TLabel', font=FONTS['subtitle'], foreground=COLORS['text_secondary'])
    
    # Button styles
    style.configure('Primary.TButton',
                   background=COLORS['primary'],
                   foreground='white',
                   borderwidth=1,
                   focuscolor=COLORS['primary_dark'],
                   padding=(20, 10),
                   font=FONTS['body'])
    style.map('Primary.TButton',
              background=[('active', COLORS['primary_dark']),
                         ('pressed', COLORS['primary_dark'])])
    
    style.configure('Secondary.TButton',
                   background=COLORS['secondary'],
                   foreground='white',
                   borderwidth=1,
                   padding=(20, 10),
                   font=FONTS['body'])
    style.map('Secondary.TButton',
              background=[('active', '#5a6268'),
                         ('pressed', '#5a6268')])
    
    style.configure('Success.TButton',
                   background=COLORS['success'],
                   foreground='white',
                   borderwidth=1,
                   padding=(20, 10),
                   font=FONTS['body'])
    style.map('Success.TButton',
              background=[('active', '#218838'),
                         ('pressed', '#218838')])
    
    style.configure('Danger.TButton',
                   background=COLORS['danger'],
                   foreground='white',
                   borderwidth=1,
                   padding=(20, 10),
                   font=FONTS['body'])
    style.map('Danger.TButton',
              background=[('active', '#c82333'),
                         ('pressed', '#c82333')])
    
    style.configure('Warning.TButton',
                   background=COLORS['warning'],
                   foreground=COLORS['dark'],
                   borderwidth=1,
                   padding=(20, 10),
                   font=FONTS['body'])
    style.map('Warning.TButton',
              background=[('active', '#e0a800'),
                         ('pressed', '#e0a800')])
    
    # Entry styles
    style.configure('TEntry', fieldbackground=COLORS['surface'], borderwidth=1)
    
    # Scrollbar styles
    style.configure('TScrollbar', background=COLORS['surface'])

def create_modern_button(parent, text, command, style='Primary.TButton', width=20):
    """Create a professionally styled button"""
    from tkinter import ttk
    btn = ttk.Button(parent, text=text, command=command, style=style, width=width)
    return btn

def create_modern_frame(parent, padding=20, style='TFrame'):
    """Create a professionally styled frame"""
    from tkinter import ttk
    return ttk.Frame(parent, padding=padding, style=style)

def create_section_label(parent, text):
    """Create a section header label"""
    from tkinter import ttk
    return ttk.Label(parent, text=text, style='Header.TLabel')