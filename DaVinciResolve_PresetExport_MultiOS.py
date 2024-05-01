#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Export all API capable custom presets of the current resolve database to a given location
'''

import sys

preset_export_path = input("enter destination directory for resulting preset exports and press enter: \n")

# load resolve
def load_resolve():
    # Set the path to the DaVinci Resolve Scripting API accordingly
    if sys.platform.startswith("win"):
        sys.path.append("C:/ProgramData/Blackmagic Design/DaVinci Resolve/Support/Developer/Scripting/Modules/")
    elif sys.platform.startswith("darwin"):
        sys.path.append("/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules/")
    elif sys.platform.startswith("linux"):
        sys.path.append("/opt/resolve/libs/Fusion/")

    try:
        import DaVinciResolveScript as dvr_script
        print("DaVinciResolveScript module loaded successfully.")
    except ImportError as e:
        print("Error loading DaVinciResolveScript module:", e)
        sys.exit(1)

    # Attempt to initialize the DaVinci Resolve application
    resolve = dvr_script.scriptapp("Resolve")
    if resolve is None:
        print("Could not initialize the DaVinci Resolve application. Is DaVinci Resolve open?")
    else:
        print("DaVinci Resolve application successfully initialized.")

    # Attempt to get the ProjectManager object
    project_manager = resolve.GetProjectManager()
    if project_manager is None:
        print("Could not access the ProjectManager.")
    else:
        print("ProjectManager successfully retrieved.")

    # Attempt to get the current project
    project = project_manager.GetCurrentProject()
    if project is None:
        print("No current project loaded.")
    else:
        print(f"Current project '{project.GetName()}' successfully loaded.")

    return dvr_script, resolve, project_manager, project

# basis resolve loading
dvr_script, resolve, project_manager, project = load_resolve()


# check version => requires at least DaVinci Resolve 18.6.4
rversion = resolve.GetVersion()
rversion_maj = rversion[0]
rversion_min = rversion[1]
rversion_pat = rversion[2]


if rversion_maj < 18:
    print ("resolve version not compatible, requires at least 18.6.4")
    exit()
if rversion_maj == 18 and rversion_min >= 4:
    print ("resolve version compatible")
if rversion_maj > 18 :
    print ("resolve version newer than expected, script might work, but was tested on 18.6.6")


render_preset_list = project.GetRenderPresetList()

for render_preset in render_preset_list:
    resolve.ExportRenderPreset(render_preset, preset_export_path)
    print(f"exported {render_preset} to {preset_export_path}")

