import requests
import os
import subprocess
from PyQt6.QtCore import QTimer
from urllib.parse import urlparse

class ToolManager:
    def __init__(self):
        self.tools = [
            {"name": "Krita", "url": "https://download.krita.org/stable/krita-5.2.2.exe"},
            {"name": "Blender", "url": "https://download.blender.org/release/Blender4.4/blender-4.4.1-windows-x64.msi"},
            {"name": "FreeCAD", "url": "https://github.com/FreeCAD/FreeCAD/releases/download/0.21.2/FreeCAD-0.21.2-Windows-x86_64.7z"},
            {"name": "R", "url": "https://cran.r-project.org/bin/windows/base/R-4.4.1-win.exe"},
            {"name": "LibreOffice", "url": "https://download.documentfoundation.org/libreoffice/stable/24.8.2/win/x86_64/LibreOffice_24.8.2_Win_x64.msi"},
            {"name": "Zettlr", "url": "https://github.com/Zettlr/Zettlr/releases/download/v3.2.0/Zettlr-3.2.0-win-x64.exe"}
        ]
        self.installed_paths = {
            "Krita": "C:\\Program Files\\Krita (x64)\\bin\\krita.exe",
            "Blender": "C:\\Program Files\\Blender Foundation\\Blender 4.4\\blender.exe",
            "FreeCAD": "C:\\Program Files\\FreeCAD\\bin\\FreeCAD.exe",
            "R": "C:\\Program Files\\R\\R-4.4.1\\bin\\R.exe",
            "LibreOffice": "C:\\Program Files\\LibreOffice\\program\\swriter.exe",
            "Zettlr": "C:\\Program Files\\Zettlr\\Zettlr.exe"
        }

    def find_blender_path(self):
        possible_paths = [
            "C:\\Program Files\\Blender Foundation\\Blender 4.4\\blender.exe",
            "C:\\Program Files\\Blender Foundation\\Blender 4.2\\blender.exe",
            "C:\\Program Files\\Blender Foundation\\Blender\\blender.exe",
            "C:\\Program Files\\Blender\\blender.exe",
            "C:\\Program Files (x86)\\Blender Foundation\\Blender\\blender.exe"
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
        # 递归搜索 Program Files
        for root, _, files in os.walk("C:\\Program Files"):
            if "blender.exe" in files:
                return os.path.join(root, "blender.exe")
        for root, _, files in os.walk("C:\\Program Files (x86)"):
            if "blender.exe" in files:
                return os.path.join(root, "blender.exe")
        return None

    def download_tool(self, tool_name, progress_bar, save_path=None):
        tool = next((t for t in self.tools if t["name"] == tool_name), None)
        if not tool:
            return f"Tool {tool_name} not found"
        url = tool["url"]
        try:
            response = requests.get(url, stream=True, timeout=10)
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))
            if total_size == 0:
                return f"Download failed: Empty file"
            block_size = 1024
            progress_bar.setMaximum(total_size)
            if not save_path:
                root_dir = os.path.dirname(os.path.dirname(__file__))
                cache_dir = os.path.join(root_dir, "cache")
                os.makedirs(cache_dir, exist_ok=True)
                parsed_url = urlparse(url)
                file_ext = os.path.splitext(parsed_url.path)[1] or ".exe"
                save_path = os.path.join(cache_dir, f"{tool_name}{file_ext}")
            if os.path.exists(save_path):
                os.remove(save_path)
            with open(save_path, "wb") as f:
                for data in response.iter_content(block_size):
                    f.write(data)
                    progress_bar.setValue(progress_bar.value() + len(data))
            progress_bar.setVisible(False)
            return save_path
        except requests.Timeout:
            progress_bar.setVisible(False)
            return f"Download failed: Connection timed out"
        except requests.ConnectionError:
            progress_bar.setVisible(False)
            return f"Download failed: Network error"
        except requests.RequestException as e:
            progress_bar.setVisible(False)
            return f"Download failed: {str(e)}"
        except IOError as e:
            progress_bar.setVisible(False)
            return f"Download failed: File error {str(e)}"

    def install_tool(self, tool_name, file_path):
        try:
            if not os.path.exists(file_path):
                return f"File {file_path} not found. Please download {tool_name} first."
            file_ext = os.path.splitext(file_path)[1].lower()
            abs_path = os.path.abspath(file_path)
            if file_ext == ".exe":
                subprocess.run([abs_path, "/S"], check=True, timeout=300)
            elif file_ext == ".msi":
                subprocess.run(["msiexec", "/i", abs_path], check=True, timeout=300)
            else:
                return f"Unsupported file type: {file_ext}"
            return f"Installed {tool_name}"
        except subprocess.CalledProcessError as e:
            if e.returncode == 1602:
                return "Installation cancelled by user. Please complete the installation wizard."
            if e.returncode == 1619:
                return "Installation failed: Cannot open installer. Try running as administrator or check file."
            return f"Installation failed: Exit code {e.returncode}"
        except PermissionError:
            return "Permission denied: Run program as administrator"
        except subprocess.TimeoutExpired:
            return f"Installation timed out after 300 seconds"
        except FileNotFoundError:
            return f"File not found: {abs_path}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"

    def launch_tool(self, tool_name):
        install_path = self.installed_paths.get(tool_name)
        if tool_name == "Blender":
            install_path = self.find_blender_path()
        if not install_path or not os.path.exists(install_path):
            return f"Tool {tool_name} not installed or path not found. Please check installation at C:\\Program Files."
        try:
            subprocess.run([install_path], check=True)
            return f"Launched {tool_name}"
        except subprocess.CalledProcessError as e:
            return f"Launch failed: {str(e)}"
