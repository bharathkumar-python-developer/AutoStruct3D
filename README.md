# AutoStruct3D
AutoStruct3D is a Python-based platform that automates the generation of 3D building models for construction applications. The system takes user-defined requirements like number of rooms, bathroom count, size, cupboard inclusion, and color preferences, and then automatically creates fully-featured 3D models in formats like .obj and .stl.

✅ 1. Introduction
1.1 Purpose
AutoStruct3D is a Python-based platform that automates the generation of 3D building models for construction applications. The system takes user-defined requirements like number of rooms, bathroom count, size, cupboard inclusion, and color preferences, and then automatically creates fully-featured 3D models in formats like .obj and .stl.
1.2 Scope
Fully automated generation of 3D buildings from structured inputs (JSON/CSV)
Support for parametric design
Intelligent reuse of prior design patterns for optimization
Export-ready formats for use in CAD or simulation
Integrates learned layouts from previous models for improved automation
Prevents logical and geometric overlaps via internal validation
1.3 Users
Civil Engineers
Architects
Construction Planners
Educational Institutes

🌐 2. Functional Requirements
ID
Feature
Description
F1
Accept user inputs
Rooms, bathrooms, cupboards, colors, direction
F2
Parametric building generation
Width, height, orientation
F3
Intelligent layout optimization
Spacing, light, door direction
F4
Auto door/window/cupboard placement
Based on rules
F5
Export 3D models
.obj, .stl
F6
Save project history for reuse
JSON storage
F7
Rule engine override
Modify behaviors via config
F8
Integrate visual material coloring
Room-specific themes/colors
F9
Learn and suggest from prior builds
Similar config = optimized layout reuse
F10
Calculate floor area and fit
Checks plot dimensions and constraints


🔒 3. Non-Functional Requirements
ID
Requirement
NFR1
Python-only implementation
NFR2
Cross-platform: Windows, macOS, Linux
NFR3
Export time < 5 seconds
NFR4
Modular design for extensibility
NFR5
Supports previous design caching


🔹 4. Inputs & Outputs
Sample Input (JSON)
{
  "rooms": 3,
  "bedroom_size": [4, 4],
  "bathrooms": 2,
  "bathroom_size": [2.5, 2],
  "cupboards": true,
  "colors": {
    "bedroom": "lightblue",
    "bathroom": "white",
    "walls": "gray"
  },
  "door_direction": "east",
  "floor_height": 3.1
}

Sample Output
model.obj
model_config.json
layout_plan.svg
preview.png

📊 5. Project Flowchart
+-------------------------------+
|        User Input Form        |
+-------------------------------+
              |
              v
+-------------------------------+
|    Input Parser & Validator   |
+-------------------------------+
              |
              v
+-------------------------------+
|  Retrieve Previous Model Data |
+-------------------------------+
              |
              v
+-------------------------------+
|  Layout + Fixture Optimizer   |
+-------------------------------+
              |
              v
+-------------------------------+
|    3D Geometry Builder Core   |
+-------------------------------+
              |
              v
+-------------------------------+
| Exporter (.OBJ/.STL/.SVG)     |
+-------------------------------+
              |
              v
+-------------------------------+
| Project Folder + Save + Log   |
+-------------------------------+



🌟 6. Future Enhancements
● GUI-based interactive design builder
● Roof, staircase, and compound modeling
● BIM/IFC/DXF support for architectural tools
● Structural simulation (load zones, wind, material types)
● API for integration with online planning tools

🕯️ 7. Conclusion
☆ AutoStruct3D delivers a high-accuracy, intelligent, and reusable modeling system for civil construction projects. With full Python compatibility, smart optimization, and a data-driven design engine, it offers professional-level 3D modeling automation for construction, education, and planning workflows.
