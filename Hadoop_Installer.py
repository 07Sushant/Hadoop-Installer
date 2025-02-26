import os
import shutil
import zipfile
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import gdown
from PIL import Image, ImageTk
import threading
import tempfile
import webbrowser

# Custom theme and styling
class ModernUI:
    PRIMARY_COLOR = "#2B6DF0"  # Blue
    SECONDARY_COLOR = "#F0F4F9"  # Light gray/blue
    ACCENT_COLOR = "#28CC85"  # Green
    TEXT_COLOR = "#2D3748"  # Dark gray
    LIGHT_TEXT = "#FFFFFF"  # White
    
    @staticmethod
    def setup_theme():
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure the buttons
        style.configure('TButton', 
                        font=('Segoe UI', 10, 'bold'),
                        background=ModernUI.PRIMARY_COLOR,
                        foreground=ModernUI.LIGHT_TEXT,
                        borderwidth=0,
                        focusthickness=3,
                        focuscolor=ModernUI.PRIMARY_COLOR)
        
        style.map('TButton',
                 background=[('active', ModernUI.PRIMARY_COLOR), 
                             ('pressed', '#1B5DF0')],
                 foreground=[('active', ModernUI.LIGHT_TEXT), 
                             ('pressed', ModernUI.LIGHT_TEXT)])

def animate_dots(label, text, is_active, delay=500):
    if not is_active[0]:
        return
    
    dots = label.cget("text").replace(text, "")
    if len(dots) >= 3:
        new_dots = ""
    else:
        new_dots = dots + "."
    
    label.config(text=f"{text}{new_dots}")
    label.after(delay, animate_dots, label, text, is_active, delay)

def download_file(url, output_path, progress_callback=None, file_type="Hadoop"):
    try:
        download_active[0] = True
        base_text = f"Please wait, downloading {file_type}"
        status_label.config(text=f"{base_text}...", fg=ModernUI.PRIMARY_COLOR)
        animate_dots(status_label, base_text, download_active)
        
        gdown.download(url, output_path, quiet=False)
        
        download_active[0] = False
        
        if file_type == "Hadoop":
            status_label.config(text=f"Hadoop download complete! ✅", fg=ModernUI.ACCENT_COLOR)
            start_button.config(state=tk.NORMAL)
        else:
            status_label.config(text=f"{file_type} download complete! ✅", fg=ModernUI.ACCENT_COLOR)
            
    except Exception as e:
        download_active[0] = False
        status_label.config(text=f"Download Error: {str(e)}", fg="red")
        tk.messagebox.showerror("Download Error", str(e))

def extract_zip(source_file, dest_dir):
    try:
        extraction_active[0] = True
        base_text = "Please wait, extracting files"
        status_label.config(text=f"{base_text}...", fg=ModernUI.PRIMARY_COLOR)
        animate_dots(status_label, base_text, extraction_active)
        
        with zipfile.ZipFile(source_file, 'r') as zip:
            for member in zip.namelist():
                zip.extract(member, path=dest_dir)
                app.update_idletasks()
                
        # Move the zip file back to the original location
        shutil.move(source_file, os.path.dirname(source_file))
        
        extraction_active[0] = False
        status_label.config(text="Extraction Complete! Hadoop is ready to use. ✅", fg=ModernUI.ACCENT_COLOR)
        tk.messagebox.showinfo("Success", "Hadoop setup completed successfully!")
        
        # Enable the open folder button
        open_folder_button.config(state=tk.NORMAL)
        
    except Exception as e:
        extraction_active[0] = False
        status_label.config(text=f"Extraction Error: {str(e)}", fg="red")
        tk.messagebox.showerror("Error", str(e))

def start_extraction():
    file_name = "hadoop-3.2.4.zip"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    source_file = os.path.join(current_dir, file_name)
    dest_dir = r"C:\hadoopsetup"

    status_label.config(text="Creating setup directory...", fg=ModernUI.PRIMARY_COLOR)
    
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    dest_file = os.path.join(dest_dir, file_name)
    shutil.move(source_file, dest_file)
    
    # Start extraction in a separate thread
    threading.Thread(target=extract_zip, args=(dest_file, dest_dir), daemon=True).start()

def initiate_download():
    download_button.config(state=tk.DISABLED)
    file_name = "hadoop-3.2.4.zip"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    source_file = os.path.join(current_dir, file_name)
    
    # Start the download in a separate thread
    threading.Thread(
        target=download_file, 
        args=("https://drive.google.com/uc?id=1JRcnPosoJd7O-XmD6AYa6BtklbDqH8z9", source_file),
        daemon=True
    ).start()

def download_jdk():
    # Get downloads folder path
    downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
    file_name = "jdk-8u333-windows-x64.exe"
    output_path = os.path.join(downloads_folder, file_name)
    
    # Start the download in a separate thread
    threading.Thread(
        target=download_file, 
        args=("https://drive.google.com/uc?id=1zvf7oGbPId7BR_9vKFISCb4b0ILu9oem", output_path, None, "JDK"),
        daemon=True
    ).start()

def download_jre():
    # Get downloads folder path
    downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
    file_name = "jre-8u371-windows-x64.exe"
    output_path = os.path.join(downloads_folder, file_name)
    
    # Start the download in a separate thread
    threading.Thread(
        target=download_file, 
        args=("https://drive.google.com/uc?id=158bcHsvtOSE0nqNGsxenOw4rMOyuSRsQ", output_path, None, "JRE"),
        daemon=True
    ).start()

def open_hadoop_folder():
    dest_dir = r"C:\hadoopsetup"
    if os.path.exists(dest_dir):
        webbrowser.open(dest_dir)
    else:
        tk.messagebox.showerror("Error", "Hadoop folder does not exist.")

def open_instructions():
    # Create a new window
    instruction_window = tk.Toplevel(app)
    instruction_window.title("Installation Instructions")
    instruction_window.geometry("700x550")
    instruction_window.resizable(False, False)
    
    # Set background
    instruction_window.configure(bg=ModernUI.SECONDARY_COLOR)
    
    # Header frame
    header_frame = tk.Frame(instruction_window, bg=ModernUI.PRIMARY_COLOR, height=60)
    header_frame.pack(fill=tk.X)
    
    # Header title
    tk.Label(
        header_frame, 
        text="Hadoop Installation Guide", 
        font=("Segoe UI", 16, "bold"), 
        bg=ModernUI.PRIMARY_COLOR,
        fg=ModernUI.LIGHT_TEXT
    ).pack(pady=15)
    
    # Create a canvas with scrollbar for the content
    canvas = tk.Canvas(instruction_window, bg=ModernUI.SECONDARY_COLOR, highlightthickness=0)
    scrollbar = ttk.Scrollbar(instruction_window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=ModernUI.SECONDARY_COLOR)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True, padx=(30, 0), pady=20)
    scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=20)
    
    # Instructions text
    instructions_text = """
    After downloading all components, follow these steps to complete your Hadoop setup:

    1. Install the JDK and JRE from your Downloads folder:
       - JDK: [Downloads]/jdk-8u333-windows-x64.exe
       - JRE: [Downloads]/jre-8u371-windows-x64.exe

    2. Download HADOOP after downloading Click on Extract Files:
       - It will take some time to Downlaod and extract the files | Size 500MB
       - After extraction, click on Open Hadoop Folder to see the extracted files

    3. Add the following paths to your system's PATH environment variable:
    """
    
    path_entries = [
        "C:\\hadoopsetup\\hadoop-3.2.4",
        "C:\\Progra~1\\Java\\jdk-1.8",
        "%HADOOP_HOME%\\bin",
        "%JAVA_HOME%\\bin"
    ]
    
    tk.Label(
        scrollable_frame,
        text=instructions_text,
        font=("Segoe UI", 11),
        bg=ModernUI.SECONDARY_COLOR,
        fg=ModernUI.TEXT_COLOR,
        justify="left",
        anchor="w",
        wraplength=600
    ).pack(fill=tk.X, pady=(0, 10))
    
    # Path entries with copy buttons
    path_frame = tk.Frame(scrollable_frame, bg=ModernUI.SECONDARY_COLOR)
    path_frame.pack(fill=tk.X, pady=10)
    
    # Create a frame for each path entry with copy button
    for i, path in enumerate(path_entries):
        entry_frame = tk.Frame(path_frame, bg=ModernUI.SECONDARY_COLOR)
        entry_frame.pack(fill=tk.X, pady=5)
        
        # Path entry
        path_entry = tk.Entry(entry_frame, width=50, font=("Segoe UI", 10))
        path_entry.insert(0, path)
        path_entry.configure(state="readonly")
        path_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Copy button
        def create_copy_callback(entry):
            return lambda: copy_to_clipboard(entry)
        
        copy_btn = ttk.Button(
            entry_frame,
            text="Copy",
            command=create_copy_callback(path_entry)
        )
        copy_btn.pack(side=tk.LEFT)
    
    # Additional instructions
    additional_text = """
    3. Set the following system environment variables:
       - JAVA_HOME: C:\\Progra~1\\Java\\jdk-1.8
       - HADOOP_HOME: C:\\hadoopsetup\\hadoop-3.2.4

    4. Restart your computer to apply the changes.

    5. Open Command Prompt and type 'hadoop version' to verify your installation.
    """
    
    tk.Label(
        scrollable_frame,
        text=additional_text,
        font=("Segoe UI", 11),
        bg=ModernUI.SECONDARY_COLOR,
        fg=ModernUI.TEXT_COLOR,
        justify="left",
        anchor="w",
        wraplength=600
    ).pack(fill=tk.X, pady=(10, 0))
    
    # Close button
    ttk.Button(
        scrollable_frame,
        text="Close",
        command=instruction_window.destroy
    ).pack(pady=20)
    
    # Bind mousewheel to scrolling
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

def copy_to_clipboard(entry_widget):
    app.clipboard_clear()
    app.clipboard_append(entry_widget.get())
    status_label.config(text="Path copied to clipboard! ✅", fg=ModernUI.ACCENT_COLOR)
    # Reset the status after 2 seconds
    app.after(2000, lambda: status_label.config(text="Ready to set up Hadoop", fg=ModernUI.TEXT_COLOR))

def open_linkedin():
    webbrowser.open("https://www.linkedin.com/in/07sushant")

# GUI setup
app = tk.Tk()
app.title('Hadoop Setup Wizard')
app.geometry('650x600')  # Increased size to accommodate more buttons
app.resizable(False, False)

# Set up modern UI theme
ModernUI.setup_theme()

# Create a background frame
bg_frame = tk.Frame(app, bg=ModernUI.SECONDARY_COLOR)
bg_frame.place(x=0, y=0, relwidth=1, relheight=1)

# Header frame
header_frame = tk.Frame(bg_frame, bg=ModernUI.PRIMARY_COLOR, height=80)
header_frame.pack(fill=tk.X)

# App title
tk.Label(
    header_frame, 
    text="Hadoop Setup Wizard", 
    font=("Segoe UI", 18, "bold"), 
    bg=ModernUI.PRIMARY_COLOR,
    fg=ModernUI.LIGHT_TEXT
).pack(pady=20)

# Main content frame
content_frame = tk.Frame(bg_frame, bg=ModernUI.SECONDARY_COLOR)
content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)

# Logo/Icon
try:
    # Try to create a simple Hadoop elephant logo using a colored circle
    logo_canvas = tk.Canvas(content_frame, width=80, height=80, bg=ModernUI.SECONDARY_COLOR, highlightthickness=0)
    logo_canvas.pack(pady=10)
    
    # Draw a stylized "H" to represent Hadoop
    logo_canvas.create_oval(10, 10, 70, 70, fill=ModernUI.PRIMARY_COLOR, outline="")
    logo_canvas.create_text(40, 40, text="H", fill=ModernUI.LIGHT_TEXT, font=("Arial", 36, "bold"))
    
except Exception:
    pass  # If there's any issue with creating the logo, just skip it

# Status label
status_label = tk.Label(
    content_frame, 
    text="Ready to set up Hadoop", 
    font=("Segoe UI", 12),
    bg=ModernUI.SECONDARY_COLOR,
    fg=ModernUI.TEXT_COLOR
)
status_label.pack(pady=(10, 20))

# Create flags for animation control
download_active = [False]
extraction_active = [False]

# Status frame (replaces progress bars)
status_frame = tk.Frame(content_frame, bg=ModernUI.SECONDARY_COLOR, height=100)
status_frame.pack(fill=tk.X, pady=20)

# Add some spacing where progress bars used to be
spacing_label = tk.Label(
    status_frame, 
    text="The setup will download and extract Hadoop.\nDownload JDK and JRE to complete the installation.",
    font=("Segoe UI", 10),
    bg=ModernUI.SECONDARY_COLOR,
    fg=ModernUI.TEXT_COLOR,
    justify=tk.CENTER
)
spacing_label.pack(fill=tk.X, pady=20)

# Button frame for Hadoop download and extraction
hadoop_button_frame = tk.Frame(content_frame, bg=ModernUI.SECONDARY_COLOR)
hadoop_button_frame.pack(fill=tk.X, pady=5)

# Hadoop Buttons
download_button = ttk.Button(
    hadoop_button_frame, 
    text="Download Hadoop", 
    command=initiate_download
)
download_button.pack(side=tk.LEFT, padx=5)

start_button = ttk.Button(
    hadoop_button_frame, 
    text="Extract Files", 
    command=start_extraction, 
    state=tk.DISABLED
)
start_button.pack(side=tk.LEFT, padx=5)

open_folder_button = ttk.Button(
    hadoop_button_frame, 
    text="Open Hadoop Folder", 
    command=open_hadoop_folder,
    state=tk.DISABLED
)
open_folder_button.pack(side=tk.LEFT, padx=5)

# Button frame for JDK/JRE downloads
jvm_button_frame = tk.Frame(content_frame, bg=ModernUI.SECONDARY_COLOR)
jvm_button_frame.pack(fill=tk.X, pady=5)

jdk_button = ttk.Button(
    jvm_button_frame, 
    text="Download JDK 8", 
    command=download_jdk
)
jdk_button.pack(side=tk.LEFT, padx=5)

jre_button = ttk.Button(
    jvm_button_frame, 
    text="Download JRE", 
    command=download_jre
)
jre_button.pack(side=tk.LEFT, padx=5)

instructions_button = ttk.Button(
    jvm_button_frame, 
    text="Installation Instructions", 
    command=open_instructions
)
instructions_button.pack(side=tk.LEFT, padx=5)

# Footer frame
footer_frame = tk.Frame(bg_frame, bg=ModernUI.SECONDARY_COLOR, height=40)
footer_frame.pack(fill=tk.X, side=tk.BOTTOM)

# Credit text with hyperlink
credit_label = tk.Label(
    footer_frame, 
    text="Made with❤️by  07Sushant", 
    font=("Segoe UI", 9), 
    bg=ModernUI.SECONDARY_COLOR,
    fg=ModernUI.PRIMARY_COLOR,
    cursor="hand2"
)
credit_label.pack(pady=10)
credit_label.bind("<Button-1>", lambda e: open_linkedin())

app.mainloop()