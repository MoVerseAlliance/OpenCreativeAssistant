def load_modules():
    return [
        {
            "name": "DCC",
            "tools": ["Krita", "Blender", "Natron", "Kdenlive", "Ardour"],
            "workflow": [
                {"name": "2D Concept", "tool": "Krita"},
                {"name": "3D Modeling", "tool": "Blender"},
                {"name": "Rendering", "tool": "Blender"},
                {"name": "Compositing", "tool": "Natron"},
                {"name": "Editing", "tool": "Kdenlive"},
                {"name": "Audio", "tool": "Ardour"}
            ]
        },
        {
            "name": "Industrial Design",
            "tools": ["FreeCAD", "LibreCAD", "OpenSCAD", "MeshLab", "Blender"],
            "workflow": [
                {"name": "2D Sketch", "tool": "LibreCAD"},
                {"name": "3D Modeling", "tool": "FreeCAD"},
                {"name": "Optimization", "tool": "MeshLab"}
            ]
        },
        {
            "name": "Data Visualization",
            "tools": ["R", "ParaView", "Matplotlib", "Blender"],
            "workflow": [
                {"name": "Data Processing", "tool": "R"},
                {"name": "2D Charts", "tool": "R"},
                {"name": "3D Visualization", "tool": "ParaView"},
                {"name": "Rendering", "tool": "Blender"}
            ]
        },
        {
            "name": "Writing & Documentation",
            "tools": ["LibreOffice", "Zettlr", "Scribus", "Inkscape"],
            "workflow": [
                {"name": "Drafting", "tool": "Zettlr"},
                {"name": "Document", "tool": "LibreOffice"},
                {"name": "Illustration", "tool": "Inkscape"},
                {"name": "Publishing", "tool": "Scribus"}
            ]
        }
    ]
