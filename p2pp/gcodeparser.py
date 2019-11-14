__author__ = 'Tom Van den Eede'
__copyright__ = 'Copyright 2018-2019, Palette2 Splicer Post Processing Project'
__credits__ = ['Tom Van den Eede',
               'Tim Brookman'
               ]
__license__ = 'GPLv3'
__maintainer__ = 'Tom Van den Eede'
__email__ = 'P2PP@pandora.be'

import math

import p2pp.variables as v
import p2pp.globals as app

def gcode_remove_params(gcode, params):
    removed = False
    result = ''
    rempar = ''
    p = gcode.split(' ')
    for s in p:
        if s == '':
            continue
        if not s[0] in params:
            result += s + ' '
        else:
            rempar = rempar + s + ' '
            removed = True

    result.strip(' ')
    rempar.strip(' ')
    if len(result) < 4:
        return ';--- P2PP Removed [Removed Parameters] - ' + gcode

    if removed:
        return result + ";--- P2PP Removed [Removed Parameters] - " + rempar
    else:
        return result


def get_gcode_parameter(gcode, parameter, default=None):
    fields = gcode.split()
    for parm in fields:
        if parm[0] == parameter:
            return float(parm[1:])
    return default


def filament_volume_to_length(x):
    return x / (v.filament_diameter[v.current_tool] / 2 * v.filament_diameter[v.current_tool] / 2 * math.pi)

def parse_slic3r_config():
    for idx in range(len(v.input_gcode) - 1, -1, -1):

        gcode_line = v.input_gcode[idx]

        if gcode_line.startswith("G1"):
            break

        if gcode_line.startswith("; wipe_tower_x"):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                v.wipetower_posx = float(gcode_line[parameter_start + 1:].strip())

        if gcode_line.startswith("; wipe_tower_width"):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                v.wipetower_width = float(gcode_line[parameter_start + 1:].strip())

        if gcode_line.startswith("; wipe_tower_y"):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                v.wipetower_posy = float(gcode_line[parameter_start + 1:].strip())

        if gcode_line.startswith("; extrusion_width"):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                v.extrusion_width = float(gcode_line[parameter_start + 1:].strip())

        if gcode_line.startswith("; infill_speed"):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                v.infill_speed = float(gcode_line[parameter_start + 1:].strip()) * 60

        if gcode_line.startswith("; layer_height"):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                v.layer_height = float(gcode_line[parameter_start + 1:].strip())

        if gcode_line.startswith("; extruder_colour") or gcode_line.startswith("; filament_colour"):
            filament_colour = ''
            parameter_start = gcode_line.find("=")
            gcode_line = gcode_line[parameter_start + 1:].strip()
            parameter_start = gcode_line.find("#")
            if parameter_start != -1:
                filament_colour = gcode_line.split(";")
            if len(filament_colour) == 4:
                for i in range(4):
                    if filament_colour[i] == "":
                        filament_colour[i] = v.filament_color_code[i]
                    else:
                        v.filament_color_code[i] = filament_colour[i][1:]


        if gcode_line.startswith("; filament_diameter"):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                filament_diameters = gcode_line[parameter_start + 1:].strip(" ").split(",")
                if len(filament_diameters) == 4:
                    for i in range(4):
                        v.filament_diameter[i] = float(filament_diameters[i])

        if gcode_line.startswith("; filament_type"):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                filament_string = gcode_line[parameter_start + 1:].strip(" ").split(";")
                if len(filament_string) == 4:
                    v.filament_type = filament_string
                    v.used_filament_types = list(set(filament_string))
            continue

        if gcode_line.startswith("; retract_lift = "):
            lift_error = False
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                retracts = gcode_line[parameter_start + 1:].strip(" ").split(",")
                if len(retracts) == 4:
                    for i in range(4):
                        v.retract_lift[i] = float(retracts[i])
                        if v.retract_lift[i] == 0:
                            lift_error = True
            continue

        if gcode_line.startswith("; retract_length = "):
            retract_error = False
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                retracts = gcode_line[parameter_start + 1:].strip(" ").split(",")
                if len(retracts) == 4:
                    for i in range(4):
                        v.retract_length[i] = float(retracts[i])
                        if v.retract_length[i] == 0.0:
                            retract_error = True
            if retract_error:
                app.log.warning(
                    "[Printer Settings]->[Extruders 1/2/3/4]->[Retraction Length] should not be set to zero.")
            continue

        if gcode_line.startswith("; gcode_flavor"):
            if "reprap" in gcode_line:
                v.isReprap_Mode = True

        if "use_firmware_retraction" in gcode_line:
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                gcode_line = gcode_line[parameter_start + 1:].replace(";", "")
                if "1" in gcode_line:
                    v.use_firmware_retraction = True
                else:
                    v.use_firmware_retraction = False

        if "use_relative_e_distances" in gcode_line:
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                gcode_line = gcode_line[parameter_start + 1:].replace(";", "")
                if "1" in gcode_line:
                    v.gcode_has_relative_e = True
                else:
                    v.gcode_has_relative_e = False

        if gcode_line.startswith("; wiping_volumes_matrix"):
            wiping_info = []
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                wiping_info = gcode_line[parameter_start + 1:].strip(" ").split(",")
                if len(wiping_info) != 16:
                    continue
                for i in range(len(wiping_info)):
                    wiping_info[i] = filament_volume_to_length(float(wiping_info[i]))
            v.max_wipe = max(wiping_info)
            if len(wiping_info) == 16:
                v.wiping_info = wiping_info
            continue
