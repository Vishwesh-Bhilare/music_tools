#!/usr/bin/env python3
try:
    import tkinter as tk
    from tkinter import ttk, messagebox, scrolledtext
    from tkinter import filedialog
except ImportError:
    print("Tkinter not available. GUI mode disabled.")
    raise

class MusicOrganizerGUI:
    def __init__(self, root, organizer):
        self.root = root
        self.organizer = organizer
        self.root.title("Music Organizer")
        self.root.geometry("800x600")
        self.setup_ui()
    
    def setup_ui(self):
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="🎵 Music Organizer", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Control buttons
        ttk.Button(main_frame, text="📁 Organize Music", 
                  command=self.organize_music).grid(row=1, column=0, pady=5, sticky=tk.W)
        
        ttk.Button(main_frame, text="⚙️ Configuration", 
                  command=self.show_config).grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Button(main_frame, text="🔄 Rescan", 
                  command=self.rescan_files).grid(row=1, column=2, pady=5, sticky=tk.E)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=2, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        
        # Log area
        self.log_area = scrolledtext.ScrolledText(main_frame, height=20, width=80)
        self.log_area.grid(row=3, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status bar
        self.status = ttk.Label(main_frame, text="Ready")
        self.status.grid(row=4, column=0, columnspan=3, pady=5, sticky=tk.W)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def log(self, message):
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.root.update()
    
    def organize_music(self):
        self.progress.start()
        self.log_area.delete(1.0, tk.END)
        self.status.config(text="Organizing music files...")
        
        try:
            self.organizer.organize_all(interactive=False)
            self.status.config(text="Organization complete!")
        except Exception as e:
            self.log(f"Error: {e}")
            self.status.config(text="Error occurred")
        finally:
            self.progress.stop()
    
    def show_config(self):
        config = self.organizer.config.data
        config_text = "\n".join([f"{k}: {v}" for k, v in config.items()])
        messagebox.showinfo("Configuration", config_text)
    
    def rescan_files(self):
        self.log_area.delete(1.0, tk.END)
        files = self.organizer.find_music_files()
        self.log(f"Found {len(files)} music files:")
        for file in files:
            self.log(f"  - {file}")

def launch_gui(organizer):
    root = tk.Tk()
    app = MusicOrganizerGUI(root, organizer)
    root.mainloop()
