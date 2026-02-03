# 🚀 Ainix Hosting v0.0.1
> **The bridge between your local code and the global web.**

**Ainix Hosting** is a simple GUI utility that automates the complexity of server configuration and public tunnelling. Whether you're demoing a new UI or testing an API, Ainix gets you online in seconds.

### *The Ultimate Local-to-Global Web Deployment Tool*

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![UI: CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-blueviolet.svg)](https://github.com/TomSchimansky/CustomTkinter)
[![Framework: Flask](https://img.shields.io/badge/Framework-Flask-lightgrey.svg)](https://flask.palletsprojects.com/)

Auto-Host is a sophisticated, Linux-optimized GUI tool designed for developers who need to transform a local directory into a globally accessible website in seconds. By combining a multi-threaded Python backend with advanced tunnelling protocols, it provides a seamless "one-click" hosting experience.

---

## 📸 Interface Preview


---

## ✨ Advanced Feature Set

### 🖥️ Modernized UI/UX
* **Adwaita-Inspired Design:** A sleek, dark-mode interface built with `CustomTkinter` that feels native to modern Linux distributions like Ubuntu, Fedora, and Arch.
* **Responsive Sidebar:** Intuitive navigation layout that separates configuration from action-based controls.
* **Dynamic Logging:** A dedicated console window that captures real-time server requests and tunnel status with millisecond-precision timestamps.

### ⚙️ Robust Server Logic
* **Multi-Threaded Architecture:** The GUI, Flask server, and Localtunnel process run on independent threads, ensuring the interface never freezes during deployment.
* **Smart Directory Mapping:** Automatically handles static assets (CSS, Images, JS), ensuring your "Glassmorphism" designs and complex scripts load perfectly.
* **Session Persistence:** Unlike basic scripts, this app stays active after a session ends, allowing for instant "Re-Launch" without restarting the Python process.

---

## 🛠️ Installation & Setup

### Clone and Install Python Stack

Download the source code and install the necessary Python libraries:

```bash
git clone https://github.com/Ainix-Hosting/ainix-hosting.git
cd ainix-hosting
pip install flask customtkinter werkzeug
```

### 🤝 Contributing

We love contributors! If you have a cool idea for a feature:

  *  **Fork the repo.**

  *  **Create your branch:** git checkout -b feature/CoolFeature

  *  **Commit changes:** git commit -m 'Add CoolFeature'

  *  **Push to branch:** git push origin feature/CoolFeature

  *  **Open a Pull Request.**

### ⚠️ Security Note

This tool is for **development** and **testing** purposes only. Tunnelling exposes a port from your local machine to the internet. Always turn off the script when you are done.




