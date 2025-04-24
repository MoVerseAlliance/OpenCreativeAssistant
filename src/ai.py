class AIRecommender:
    def recommend_tool(self, tool_name):
        recommendations = {
            "Krita": "Use Krita for PBR textures. Try the 'PBR Template' plugin.",
            "Blender": "Blender is great for 3D modeling. Check out HardOps for efficiency.",
            "FreeCAD": "FreeCAD is ideal for parametric modeling. Use the 'Part Design' workbench.",
            "R": "R with ggplot2 is perfect for charts. Try the 'theme_minimal' for clean visuals.",
            "LibreOffice": "LibreOffice is great for reports. Use the 'Writer' template for papers."
        }
        return recommendations.get(tool_name, "No recommendation available.")
