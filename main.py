import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os
import subprocess
import time
from flask import Flask, send_from_directory

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ModernServerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Auto-Host v0.0.1")
        self.geometry("800x550")
        
        # Instance variables for management
        self.web_directory = ""
        self.tunnel_process = None
        self.is_running = False

        # --- LAYOUT CONFIG ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="🚀 HOST PRO", font=ctk.CTkFont(size=22, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=30)

        self.btn_select = ctk.CTkButton(self.sidebar, text="📁 Select Folder", height=35, command=self.select_folder)
        self.btn_select.grid(row=1, column=0, padx=20, pady=10)

        self.btn_launch = ctk.CTkButton(self.sidebar, text="🚀 Launch", height=40, fg_color="#2ecc71", hover_color="#27ae60", command=self.start_server)
        self.btn_launch.grid(row=2, column=0, padx=20, pady=10)

        self.btn_stop = ctk.CTkButton(self.sidebar, text="🛑 Terminate", height=40, fg_color="#e74c3c", hover_color="#c0392b", command=self.stop_server, state="disabled")
        self.btn_stop.grid(row=3, column=0, padx=20, pady=10)

        # --- MAIN CONTENT ---
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.grid(row=0, column=1, padx=30, pady=30, sticky="nsew")

        self.status_frame = ctk.CTkFrame(self.main_content, fg_color="#1e293b", height=40)
        self.status_frame.pack(fill="x", pady=(0, 20))
        
        self.status_label = ctk.CTkLabel(self.status_frame, text="● SYSTEM STANDBY", text_color="#94a3b8", font=ctk.CTkFont(weight="bold"))
        self.status_label.pack(pady=10)

        self.path_display = ctk.CTkEntry(self.main_content, placeholder_text="No directory linked...", width=500, height=35)
        self.path_display.pack(pady=10)

        self.log_widget = ctk.CTkTextbox(self.main_content, width=500, height=280, font=("Consolas", 12), border_width=1)
        self.log_widget.pack(pady=10)

    def log(self, message):
        timestamp = time.strftime("%H:%M:%S")
        self.log_widget.insert("end", f"[{timestamp}] {message}\n")
        self.log_widget.see("end")

    def select_folder(self):
        self.web_directory = filedialog.askdirectory()
        if self.web_directory:
            self.path_display.delete(0, "end")
            self.path_display.insert(0, self.web_directory)
            self.log(f"FOLDER LINKED: {self.web_directory}")

    def run_flask(self):
        # We define a new Flask app instance inside the thread to allow restarts
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
        self.status_label.configure(text="● SYSTEM LIVE", text_color="#2ecc71")
        self.btn_launch.configure(state="disabled")
        self.btn_stop.configure(state="normal")
        
        # Start Threads
        threading.Thread(target=self.run_flask, daemon=True).start()
        threading.Thread(target=self.start_tunnel, daemon=True).start()
        self.log("INITIATING: Server & Tunnel deployment...")

    def stop_server(self):
        self.is_running = False
        
        # Kill the tunnel process
        if self.tunnel_process:
            self.tunnel_process.terminate()
            self.tunnel_process = None
        
        # Update UI
        self.log("TERMINATED: Web server and tunnel shut down.")
        self.status_label.configure(text="● SESSION ENDED", text_color="#e74c3c")
        self.btn_launch.configure(text="🚀 Re-Launch", state="normal")
        self.btn_stop.configure(state="disabled")

if __name__ == "__main__":
    app = ModernServerApp()
    app.mainloop()