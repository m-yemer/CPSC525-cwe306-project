'''
Reusable professional GUI components
'''

def set_user_label(lbl, CURRENT_USER):
    """Update user status label professionally"""
    from .gui_styles import COLORS, FONTS
    if CURRENT_USER:
        admin_status = " (Administrator)" if CURRENT_USER.get("is_admin") else ""
        lbl.config(text=f"User: {CURRENT_USER['username']}{admin_status}", 
                  foreground=COLORS['primary'],
                  font=FONTS['body'])
    else:
        lbl.config(text="User: Not logged in", 
                  foreground=COLORS['text_secondary'],
                  font=FONTS['body'])

def create_header(parent, title, subtitle=None):
    """Create a professional header section"""
    from tkinter import ttk
    from .gui_styles import create_modern_frame
    
    header_frame = create_modern_frame(parent, 25)
    header_frame.pack(fill='x', padx=40, pady=(30, 20))
    
    # Title
    title_label = ttk.Label(header_frame, text=title, style='Title.TLabel')
    title_label.pack(anchor='center', pady=(0, 8))
    
    # Subtitle (optional)
    if subtitle:
        subtitle_label = ttk.Label(header_frame, text=subtitle, style='Subtitle.TLabel')
        subtitle_label.pack(anchor='center')
    
    return header_frame

def create_scrolled_text(parent, width=80, height=20, font=('Consolas', 10)):
    """Create a professional scrolled text widget"""
    from tkinter import scrolledtext
    from .gui_styles import COLORS
    
    text_widget = scrolledtext.ScrolledText(
        parent, 
        width=width, 
        height=height,
        font=font,
        bg=COLORS['surface'],
        relief='solid',
        borderwidth=1,
        padx=12,
        pady=12,
        wrap='word'
    )
    return text_widget

def center_window(window):
    """Center any window on the screen"""
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

def create_dialog_header(parent, title):
    """Create a header for dialog windows"""
    from tkinter import ttk
    from .gui_styles import FONTS, COLORS
    
    header_frame = ttk.Frame(parent)
    header_frame.pack(fill='x', pady=(0, 20))
    
    title_label = ttk.Label(header_frame, text=title, 
                           font=FONTS['title'], 
                           foreground=COLORS['primary'])
    title_label.pack(anchor='center')
    
    return header_frame

def create_form_field(parent, label_text, widget_type='entry', default_value='', width=25):
    """Create a standardized form field"""
    from tkinter import ttk, StringVar, BooleanVar
    from .gui_styles import FONTS
    
    field_frame = ttk.Frame(parent)
    field_frame.pack(fill='x', pady=8)
    
    # Label
    label = ttk.Label(field_frame, text=label_text, style='Header.TLabel')
    label.pack(anchor='w', pady=(0, 5))
    
    # Widget
    if widget_type == 'entry':
        var = StringVar(value=default_value)
        widget = ttk.Entry(field_frame, textvariable=var, width=width, font=FONTS['body'])
        widget.pack(fill='x')
        return var, widget
    elif widget_type == 'password':
        var = StringVar(value=default_value)
        widget = ttk.Entry(field_frame, textvariable=var, show='*', width=width, font=FONTS['body'])
        widget.pack(fill='x')
        return var, widget
    elif widget_type == 'checkbox':
        var = BooleanVar(value=default_value)
        widget = ttk.Checkbutton(field_frame, text=label_text, variable=var)
        widget.pack(anchor='w')
        return var, widget
    
    return None, None