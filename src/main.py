import sys
import json
import os
from PyQt6.QtWidgets import QApplication
from ui import MainWindow
from modules import load_modules
from config import CONFIG_FILE

def main():
    # 确保配置文件存在
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as f:
            json.dump({"modules": [], "theme": "dark", "language": "en"}, f)

    # 初始化应用
    app = QApplication(sys.argv)
                                                    
    # 加载模块
    modules = load_modules()
                                                                
    # 创建主窗口
    window = MainWindow(modules)
    window.show()
                                                                                
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
