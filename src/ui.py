from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QListWidget, QPushButton, QTextEdit, QLabel, 
                             QProgressBar, QFileDialog, QComboBox, QFrame)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPalette, QColor, QLinearGradient, QGradient, QFont
from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from workflow_manager import WorkflowManager
from tools import ToolManager
from ai import AIRecommender
import os
import logging

# 设置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedHeight(32)
        self.setStyleSheet("""
            background-color: #1E1E2E;
            border-bottom: 1px solid #42A5F5;
        """)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(5)

        # 标题
        title = QLabel("OpenCreativeAssistant")
        title.setStyleSheet("""
            color: #FFFFFF;
            font-family: Consolas;
            font-size: 16px;
            font-weight: bold;
        """)
        layout.addWidget(title)
        layout.addStretch()

        # 最小化按钮
        min_btn = QPushButton("−")
        min_btn.setFixedSize(20, 20)
        min_btn.setStyleSheet("""
            QPushButton {
                background-color: #3C4B64;
                color: #FFFFFF;
                border: none;
                border-radius: 3px;
                font-family: Consolas;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #42A5F5 !important;
            }
            QPushButton:pressed {
                transform: scale(0.95);
            }
        """)
        min_btn.clicked.connect(parent.showMinimized)
        layout.addWidget(min_btn)

        # 关闭按钮
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(20, 20)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #3C4B64;
                color: #FFFFFF;
                border: none;
                border-radius: 3px;
                font-family: Consolas;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #EF5350 !important;
            }
            QPushButton:pressed {
                transform: scale(0.95);
            }
        """)
        close_btn.clicked.connect(parent.close)
        layout.addWidget(close_btn)

class MainWindow(QMainWindow):
    def __init__(self, modules):
        super().__init__()
        self.setWindowTitle("OpenCreativeAssistant")
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # 移除默认标题栏
        self.modules = modules
        self.workflow_manager = WorkflowManager()
        self.tool_manager = ToolManager()
        self.ai_recommender = AIRecommender()
        self._last_download_path = None
        logger.debug("Initializing UI")
        self.init_ui()

    def init_ui(self):
        # 主容器
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 自定义标题栏
        self.title_bar = CustomTitleBar(self)
        main_layout.addWidget(self.title_bar)

        # 内容区域
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.setSpacing(10)

        # 设置背景
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, 800)
        gradient.setColorAt(0, QColor(30, 30, 46))  # 深灰
        gradient.setColorAt(1, QColor(37, 37, 53))  # 略浅灰
        palette.setBrush(QPalette.ColorRole.Window, gradient)
        self.setPalette(palette)

        # 全局样式表
        self.setStyleSheet("""
            QWidget {
                font-family: Consolas;
                font-size: 14px;
            }
            QPushButton {
                background-color: #3C4B64;
                color: #FFFFFF;
                border: 1px solid #42A5F5;
                border-radius: 5px;
                padding: 8px;
                margin: 5px;
                transition: all 0.2s;
            }
            QPushButton:hover {
                background-color: #42A5F5 !important;
                border: 1px solid #64B5F6 !important;
                color: #FFFFFF !important;
            }
            QPushButton:pressed {
                transform: scale(0.98);
            }
            #downloadBtn:hover, #installBtn:hover, #launchBtn:hover {
                background-color: #42A5F5 !important;
                border: 1px solid #64B5F6 !important;
                color: #FFFFFF !important;
            }
            QComboBox {
                background-color: #2A2A3A;
                color: #FFFFFF;
                border: 1px solid #42A5F5;
                border-radius: 5px;
                padding: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: #3A3A4A;
                color: #FFFFFF;
                selection-background-color: #42A5F5;
                selection-color: #FFFFFF;
                border: 1px solid #42A5F5;
                border-radius: 5px;
            }
            QListWidget, QTextEdit {
                background-color: #2A2A3A;
                color: #FFFFFF;
                border: 1px solid #42A5F5;
                border-radius: 5px;
            }
            QProgressBar {
                background-color: #2A2A3A;
                border: 1px solid #42A5F5;
                border-radius: 5px;
                text-align: center;
                color: #FFFFFF;
            }
            QProgressBar::chunk {
                background-color: #42A5F5;
                border-radius: 5px;
            }
            QLabel {
                color: #D4D4D4;
                font-weight: bold;
            }
        """)
        logger.debug("Applied stylesheet")

        # 左侧：模块面板
        module_panel = QWidget()
        module_panel.setStyleSheet("background-color: #252535; border: 1px solid #42A5F5; border-radius: 5px;")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setOffset(2, 2)
        module_panel.setGraphicsEffect(shadow)
        module_layout = QVBoxLayout(module_panel)
        module_layout.setContentsMargins(10, 10, 10, 10)
        module_label = QLabel("Modules")
        self.module_list = QListWidget()
        for module in self.modules:
            self.module_list.addItem(module["name"])
        self.module_list.currentItemChanged.connect(self.load_module)
        module_layout.addWidget(module_label)
        module_layout.addWidget(self.module_list)
        content_layout.addWidget(module_panel, 1)

        # 中间：工作流面板
        workflow_panel = QWidget()
        workflow_panel.setStyleSheet("background-color: #252535; border: 1px solid #42A5F5; border-radius: 5px;")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setOffset(2, 2)
        workflow_panel.setGraphicsEffect(shadow)
        workflow_layout = QVBoxLayout(workflow_panel)
        workflow_layout.setContentsMargins(10, 10, 10, 10)
        workflow_label = QLabel("Workflow")
        self.stage_list = QListWidget()
        self.stage_list.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        add_stage_btn = QPushButton("Add Stage")
        add_stage_btn.clicked.connect(self.add_stage)
        workflow_layout.addWidget(workflow_label)
        workflow_layout.addWidget(self.stage_list)
        workflow_layout.addWidget(add_stage_btn)
        content_layout.addWidget(workflow_panel, 2)

        # 右侧：工具与文件面板
        tools_panel = QWidget()
        tools_panel.setStyleSheet("background-color: #252535; border: 1px solid #42A5F5; border-radius: 5px;")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setOffset(2, 2)
        tools_panel.setGraphicsEffect(shadow)
        tools_layout = QVBoxLayout(tools_panel)
        tools_layout.setContentsMargins(10, 10, 10, 10)
        tools_label = QLabel("Tools & Files")
        self.tool_combo = QComboBox()
        self.tool_combo.addItems(["Select Tool"] + [tool["name"] for tool in self.tool_manager.tools])
        self.tool_combo.currentTextChanged.connect(self.select_tool)
        download_btn = QPushButton("Download Tool")
        download_btn.setObjectName("downloadBtn")
        download_btn.clicked.connect(self.download_tool)
        install_btn = QPushButton("Install Tool")
        install_btn.setObjectName("installBtn")
        install_btn.clicked.connect(self.install_tool)
        launch_btn = QPushButton("Launch Tool")
        launch_btn.setObjectName("launchBtn")
        launch_btn.clicked.connect(self.launch_tool)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        file_btn = QPushButton("Import File")
        file_btn.clicked.connect(self.import_file)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        tools_layout.addWidget(tools_label)
        tools_layout.addWidget(self.tool_combo)
        tools_layout.addWidget(download_btn)
        tools_layout.addWidget(install_btn)
        tools_layout.addWidget(launch_btn)
        tools_layout.addWidget(self.progress_bar)
        tools_layout.addWidget(file_btn)
        tools_layout.addWidget(self.log_text)
        content_layout.addWidget(tools_panel, 2)

        # 底部：AI 推荐
        ai_panel = QWidget()
        ai_panel.setStyleSheet("background-color: #252535; border: 1px solid #42A5F5; border-radius: 5px;")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setOffset(2, 2)
        ai_panel.setGraphicsEffect(shadow)
        ai_layout = QVBoxLayout(ai_panel)
        ai_layout.setContentsMargins(10, 10, 10, 10)
        ai_label = QLabel("AI Recommendations")
        self.ai_text = QTextEdit()
        self.ai_text.setReadOnly(True)
        ai_layout.addWidget(ai_label)
        ai_layout.addWidget(self.ai_text)
        content_layout.addWidget(ai_panel, 1)

        main_layout.addWidget(content_widget, 1)

    def load_module(self):
        selected = self.module_list.currentItem()
        if selected:
            module_name = selected.text()
            self.workflow_manager.load_module(module_name, self.modules)
            self.stage_list.clear()
            for stage in self.workflow_manager.current_workflow:
                self.stage_list.addItem(stage["name"])
            self.log_text.append(f"Loaded module: {module_name}")
            logger.debug(f"Loaded module: {module_name}")

    def add_stage(self):
        stage_name = f"Stage {self.stage_list.count() + 1}"
        self.workflow_manager.add_stage(stage_name, "Select Tool")
        self.stage_list.addItem(stage_name)
        self.log_text.append(f"Added stage: {stage_name}")
        logger.debug(f"Added stage: {stage_name}")

    def select_tool(self, tool_name):
        if tool_name != "Select Tool":
            self.log_text.append(f"Selected tool: {tool_name}")
            recommendation = self.ai_recommender.recommend_tool(tool_name)
            self.ai_text.setText(recommendation)
            logger.debug(f"Selected tool: {tool_name}")

    def download_tool(self):
        tool_name = self.tool_combo.currentText()
        if tool_name != "Select Tool":
            root_dir = os.path.dirname(os.path.dirname(__file__))
            cache_dir = os.path.join(root_dir, "cache")
            os.makedirs(cache_dir, exist_ok=True)
            default_path = os.path.join(cache_dir, f"{tool_name}.msi" if tool_name in ["Blender", "LibreOffice"] else f"{tool_name}.exe")
            save_path, _ = QFileDialog.getSaveFileName(self, "Select Download Location", default_path)
            if save_path:
                self.progress_bar.setVisible(True)
                result = self.tool_manager.download_tool(tool_name, self.progress_bar, save_path)
                self.log_text.append(f"Downloaded {tool_name} to {result}")
                self._last_download_path = save_path
                logger.debug(f"Downloaded {tool_name} to {result}")

    def install_tool(self):
        tool_name = self.tool_combo.currentText()
        if tool_name != "Select Tool":
            try:
                file_path = getattr(self, '_last_download_path', None)
                if not file_path or not os.path.exists(file_path):
                    root_dir = os.path.dirname(os.path.dirname(__file__))
                    file_path = os.path.join(root_dir, "cache", f"{tool_name}.msi" if tool_name in ["Blender", "LibreOffice"] else f"{tool_name}.exe")
                if not os.path.exists(file_path):
                    self.log_text.append(f"File {file_path} not found. Please download {tool_name} to {os.path.dirname(file_path)}.")
                    logger.error(f"File {file_path} not found")
                    return
                result = self.tool_manager.install_tool(tool_name, file_path)
                self.log_text.append(result)
                logger.debug(f"Installed {tool_name}: {result}")
            except Exception as e:
                self.log_text.append(f"Install error: {str(e)}")
                logger.error(f"Install error: {str(e)}")

    def launch_tool(self):
        tool_name = self.tool_combo.currentText()
        if tool_name != "Select Tool":
            result = self.tool_manager.launch_tool(tool_name)
            self.log_text.append(result)
            logger.debug(f"Launched {tool_name}: {result}")

    def import_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Import File")
        if file_path:
            self.workflow_manager.import_file(file_path)
            self.log_text.append(f"Imported file: {file_path}")
            logger.debug(f"Imported file: {file_path}")
