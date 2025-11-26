'''
Reusable GUI components
'''

def set_user_label(lbl, CURRENT_USER):
    """Update the user label with current user info"""
    from .gui_styles import COLORS
    if CURRENT_USER:
        admin_status = " (Admin)" if CURRENT_USER.get("is_admin") else ""
        lbl.config(text=f"👤 User: {CURRENT_USER['username']}{admin_status}", 
                  foreground=COLORS['primary'])
    else:
        lbl.config(text="👤 User: Not logged in", 
                  foreground=COLORS['secondary'])

def create_header(parent, title, subtitle=None):
    """Create a modern header"""
    from tkinter import ttk
    from .gui_styles import create_modern_frame, COLORS
    
    header_frame = create_modern_frame(parent, 15)
    header_frame.pack(fill='x', padx=20, pady=20)
    
    ttk.Label(header_frame, text=title, 
             font=('Arial', 18, 'bold')).pack(anchor='w')
    
    if subtitle:
        ttk.Label(header_frame, text=subtitle,
                 font=('Arial', 12), foreground=COLORS['secondary']).pack(anchor='w')
    
    return header_frame

def create_scrolled_text(parent, width=80, height=20, font=('Consolas', 10)):
    """Create a modern scrolled text widget"""
    from tkinter import scrolledtext
    from .gui_styles import COLORS
    
    text_widget = scrolledtext.ScrolledText(parent, 
                                          width=width, 
                                          height=height,
                                          font=font,
                                          bg=COLORS['surface'],
                                          relief='flat',
                                          padx=10, pady=10)
    return text_widget