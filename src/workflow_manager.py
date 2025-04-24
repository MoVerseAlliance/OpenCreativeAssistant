import json

class WorkflowManager:
    def __init__(self):
        self.current_workflow = []
        self.current_module = None

    def load_module(self, module_name, modules):
        self.current_module = next((m for m in modules if m["name"] == module_name), None)
        if self.current_module:
            self.current_workflow = self.current_module.get("workflow", [])
        else:
            self.current_workflow = []

    def add_stage(self, stage_name, tool_name):
        self.current_workflow.append({"name": stage_name, "tool": tool_name})

    def import_file(self, file_path):
        # 模拟文件导入
        return {"path": file_path, "stage": self.current_workflow[-1]["name"] if self.current_workflow else "None"}
