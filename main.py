import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os
import subprocess
import time
import webbrowser
from flask import Flask, send_from_directory
import pystray
from PIL import Image
import sys

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ModernServerApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        # ... existing setup ...

        # Protocol to handle when user clicks the "X" button
        self.protocol("WM_DELETE_WINDOW", self.hide_window)
        self.create_tray_icon()

    def create_tray_icon(self):
        # Create a simple square icon (you can load your logo here)
        image = Image.new('RGB', (64, 64), color=(37, 99, 235))
        menu = pystray.Menu(
            pystray.MenuItem("Show Ainix", self.show_window),
            pystray.MenuItem("Quit Completely", self.quit_app)
        )
        self.tray_icon = pystray.Icon("Ainix", image, "Ainix Hosting", menu)
        
        # Start tray in a separate thread so it doesn't freeze the GUI
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def hide_window(self):
        self.withdraw() # Hides the window from the taskbar but keeps code running
        self.log("SYSTEM: Minimized to tray. Server is still active.")

    def show_window(self):
        self.deiconify() # Brings the window back

    def quit_app(self):
        self.tray_icon.stop()
        self.stop_server() # Cleanly kills the tunnel and flask
        self.destroy()
        sys.exit()

    def __init__(self):
        super().__init__()

        self.title("Ainix Hosting v0.0.1")
        self.geometry("800x580")
        
        self.web_directory = ""
        self.tunnel_process = None
        self.is_running = False

        # --- LAYOUT CONFIG ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Common Button Settings for consistency
        # This font will be used for all buttons
        btn_font = ctk.CTkFont(family="Arial", size=13, weight="bold")

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#1a1c1e")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="🚀 AINIX", font=ctk.CTkFont(size=22, weight="bold"), text_color="#ffffff")
        self.logo_label.grid(row=0, column=0, padx=20, pady=30)

        # Folder Select Button
        self.btn_select = ctk.CTkButton(self.sidebar, text="📁 Select Folder", height=35, 
                                       fg_color="#374151", hover_color="#4b5563", 
                                       text_color="#ffffff", text_color_disabled="#ffffff",
                                       font=btn_font, command=self.select_folder)
        self.btn_select.grid(row=1, column=0, padx=20, pady=10)

        # Launch Button
        self.btn_launch = ctk.CTkButton(self.sidebar, text="🚀 Launch", height=40, 
                                       fg_color="#059669", hover_color="#047857", 
                                       text_color="#ffffff", text_color_disabled="#ffffff",
                                       font=btn_font, command=self.start_server)
        self.btn_launch.grid(row=2, column=0, padx=20, pady=10)

        # View Website Button
        self.btn_browse = ctk.CTkButton(self.sidebar, text="🌐 View Website", height=40, 
                                       fg_color="#2563eb", hover_color="#1d4ed8", 
                                       text_color="#ffffff", text_color_disabled="#ffffff",
                                       font=btn_font, command=self.open_browser, state="disabled")
        self.btn_browse.grid(row=3, column=0, padx=20, pady=10)

        # Terminate Button
        self.btn_stop = ctk.CTkButton(self.sidebar, text="🛑 Terminate", height=40, 
                                     fg_color="#dc2626", hover_color="#b91c1c", 
                                     text_color="#ffffff", text_color_disabled="#ffffff",
                                     font=btn_font, command=self.stop_server, state="disabled")
        self.btn_stop.grid(row=4, column=0, padx=20, pady=10)

        # --- MAIN CONTENT ---
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.grid(row=0, column=1, padx=30, pady=30, sticky="nsew")

        self.status_frame = ctk.CTkFrame(self.main_content, fg_color="#111827", height=40, corner_radius=10)
        self.status_frame.pack(fill="x", pady=(0, 20))
        
        self.status_label = ctk.CTkLabel(self.status_frame, text="● SYSTEM STANDBY", text_color="#6b7280", font=ctk.CTkFont(weight="bold"))
        self.status_label.pack(pady=10)

        self.path_display = ctk.CTkEntry(self.main_content, placeholder_text="No directory linked...", width=500, height=35, 
                                        fg_color="#1f2937", border_color="#374151", text_color="#ffffff")
        self.path_display.pack(pady=10)

        self.log_widget = ctk.CTkTextbox(self.main_content, width=500, height=280, font=("Consolas", 12), 
                                        fg_color="#030712", text_color="#10b981", border_width=1, border_color="#1f2937")
        self.log_widget.pack(pady=10)

    # Logic Methods
    def log(self, message):
        timestamp = time.strftime("%H:%M:%S")
        self.log_widget.insert("end", f"[{timestamp}] {message}\n")
        self.log_widget.see("end")

    def open_browser(self):
        webbrowser.open("http://127.0.0.1:5000")
        self.log("[UI] Opening default browser...")

    def select_folder(self):
        self.web_directory = filedialog.askdirectory()
        if self.web_directory:
            self.path_display.delete(0, "end")
            self.path_display.insert(0, self.web_directory)
            self.log(f"FOLDER LINKED: {self.web_directory}")

    def run_flask(self):
        app = Flask(__name__)
        @app.route('/')
        def serve(): return send_from_directory(self.web_directory, 'index.html')
        @app.route('/<path:path>')
        def serve_static(path): return send_from_directory(self.web_directory, path)
        try:
            app.run(port=5000, debug=False, use_reloader=False)
        except Exception as e:
            self.log(f"SERVER ERROR: {e}")

    def start_tunnel(self):
        self.tunnel_process = subprocess.Popen(["npx", "localtunnel", "--port", "5000"], 
                                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in self.tunnel_process.stdout:
            if not self.is_running: break
            self.log(f"NETWORK: {line.strip()}")

    def start_server(self):
        if not self.web_directory:
            messagebox.showwarning("Missing Files", "Please select a folder to host first!")
            return
        self.is_running = True
        self.status_label.configure(text="● SYSTEM LIVE", text_color="#10b981")
        self.btn_launch.configure(state="disabled")
        self.btn_stop.configure(state="normal")
        self.btn_browse.configure(state="normal")
        threading.Thread(target=self.run_flask, daemon=True).start()
        threading.Thread(target=self.start_tunnel, daemon=True).start()
        self.log("INITIATING: Server & Tunnel deployment...")

    def stop_server(self):
        self.is_running = False
        if self.tunnel_process:
            self.tunnel_process.terminate()
            self.tunnel_process = None
        self.log("TERMINATED: Web server and tunnel shut down.")
        self.status_label.configure(text="● SESSION ENDED", text_color="#ef4444")
        self.btn_launch.configure(text="🚀 Re-Launch", state="normal")
        self.btn_stop.configure(state="disabled")
        self.btn_browse.configure(state="disabled")

if __name__ == "__main__":
    app = ModernServerApp()
    app.mainloop()
