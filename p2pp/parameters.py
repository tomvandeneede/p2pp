__author__ = 'Tom Van den Eede'
__copyright__ = 'Copyright 2018-2019, Palette2 Splicer Post Processing Project'
__credits__ = ['Tom Van den Eede',
               'Tim Brookman'
               ]
__license__ = 'GPLv3'
__maintainer__ = 'Tom Van den Eede'
__email__ = 'P2PP@pandora.be'

import p2pp.globals as app
import p2pp.variables as v

def floatparameter(s):
    pos = s.find("=")
    try:
        return float(s[pos + 1:])
    except ValueError:
        return 0


def stringparameter(s):
    pos = s.find("=")
    try:
        return s[pos + 1:].strip()
    except IndexError:
        return ""


def check_config_parameters(line):
    # BASIC SETUP  (material setup handled in mcf.py

    # -p takes precedence over printer defined in file
    if "PRINTERPROFILE" in line:
        tmp_string = stringparameter(line)
        if len(tmp_string) != 16:
            app.log.warning("Invalid Printer profile!  - Has invalid length (expect 16) - [{}]"
                            .format(tmp_string))
            tmp_string = ""
        if not all(char in set("0123456789ABCDEFabcdef") for char in tmp_string):
            app.log.warning("Invalid Printer profile!  - Invalid characters  (expect 0123456789abcdef) - [{}]"
                            .format(tmp_string))
            tmp_string = ""

        if len(tmp_string) == 16:
            v.printer_profile_string = tmp_string
            if v.gui:
                app.gui.set_printer_id(v.printer_profile_string)
        return

    if "ACCESSORYMODE_MAF" in line:
        v.accessory_mode = True
        app.log.info("Config: Palette2 Accessory Mode Selected")

    if "ACCESSORYMODE_MSF" in line:
        v.accessory_mode = True
        v.palette_plus = True
        app.log.info("Config: Palette+ Accessory Mode Selected")

    if "P+LOADINGOFFSET" in line:
        v.palette_plus_loading_offset = int(floatparameter(line))

    if "P+PPM" in line:
        v.palette_plus_ppm = int(floatparameter(line))

    if "SPLICEOFFSET" in line:
        v.splice_offset = floatparameter(line)
        app.log.info("Splice Offset set to {:-5.2f}mm".format(v.splice_offset))
        return

    if "PROFILETYPEOVERRIDE" in line:
        v.filament_type[v.current_tool] = stringparameter(line)
        v.used_filament_types.append(v.filament_type[v.current_tool])
        v.used_filament_types = list(dict.fromkeys(v.used_filament_types))
        return

    if "EXTRUSIONMULTIPLIERCORRECTION" in line:
        v.filament_type[v.current_tool] = floatparameter(line)
        return

    if "EXTRAENDFILAMENT" in line:
        v.extra_runout_filament = floatparameter(line)
        app.log.info("Extra filament at end of print {:-8.2f}mm".format(v.extra_runout_filament))
        return

    if "BEFORESIDEWIPEGCODE" in line:
        v.before_sidewipe_gcode.append(stringparameter(line))
        return

    if "AFTERSIDEWIPEGCODE" in line:
        v.after_sidewipe_gcode.append(stringparameter(line))
        return

    if "MINSTARTSPLICE" in line:
        v.min_start_splice_length = floatparameter(line)
        if v.min_start_splice_length < 100:
            v.min_start_splice_length = 100
            app.log.warning("Minimal first slice length adjusted to 100mm")
        return

    if "BEDSIZEX" in line:
        v.bed_size_x = floatparameter(line)
        return
    if "BEDSIZEY" in line:
        v.bed_size_y = floatparameter(line)
        return
    if "BEDORIGINX" in line:
        v.bed_origin_x = floatparameter(line)
        return
    if "BEDORIGINY" in line:
        v.bed_origin_y = floatparameter(line)
        return

    if "BIGBRAIN3D_BLOBSIZE" in line:
        v.bigbrain3d_blob_size = int(floatparameter(line))

    if "BIGBRAIN3D_COOLINGTIME" in line:
        v.bigbrain3d_blob_cooling_time = int(floatparameter(line))

    if "BIGBRAIN3D_PURGEPOSITION" in line:
        v.bigbrain3d_x_position = floatparameter(line)

    if "BIGBRAIN3D_ENABLE" in line:
        v.bigbrain3d_purge_enabled = True
        app.log.warning("BIGBRAIN3D Will only work with installed hardware on a Prusa Printer")

    if "MINSPLICE" in line:
        v.min_splice_length = floatparameter(line)
        if v.min_splice_length < 70:
            v.min_splice_length = 70
            app.log.warning("Minimal slice length adjusted to 70mm")
        return

    # LINEAR PING removed

    if "LINEARPINGLENGTH" in line:
        v.ping_interval = floatparameter(line)
        v.ping_length_multiplier = 1.0
        if v.ping_interval < 300:
            v.ping_interval = 300
            app.log.warning("Minimal Linear Ping distance is 300mm!  Your config stated: {}".format(line))
        app.log.info("Linear Ping interval of  {:-6.2f}mm".format(v.ping_interval))
        return

    if line.endswith("LINEARPING"):
        app.log.warning("LINEARPING deprecated, use LINEARPINGLENGTH  parameter instead")
        return

    # SIDE TRANSITIONING
    if "SIDEWIPELOC" in line:
        v.side_wipe_loc = stringparameter(line)
        return

    if "WIPEFEEDRATE" in line:
        v.wipe_feedrate = floatparameter(line)
        return

    if "SIDEWIPEMINY" in line:
        v.sidewipe_miny = floatparameter(line)
        return

    if "SIDEWIPEMAXY" in line:
        v.sidewipe_maxy = floatparameter(line)
        return

    if "SIDEWIPECORRECTION" in line:
        v.sidewipe_correction = floatparameter(line)
        if v.sidewipe_correction < 0.9 or v.sidewipe_correction > 1.10:
            v.sidewipe_correction = 1.0
        return

    if "PURGETOWERDELTA" in line:
        if abs(floatparameter(line)) != abs(float(0)):
            v.max_tower_z_delta = abs(floatparameter(line))
            app.log.info("Max Purge Tower Delta set to {:-2.2f}mm".format(v.max_tower_z_delta))
        return
    if "FULLPURGEREDUCTION" in line:
        app.log.info("Full purge reduction configured")
        v.full_purge_reduction = True

    if line.endswith("CHECKVERSION"):
        import p2pp.checkversion as cv
        import version
        latest = cv.get_version(cv.MASTER)
        if latest > version.Version:
            app.log.info("New development version of P2PP available ({})".format(latest), "red", False, "2.0")
        else:
            if (latest < version.Version):
                latest = cv.get_version(cv.DEV)
                if (latest > version.Version):
                    app.log.info("New development version of P2PP available ({})".format(latest), "red", False,
                                       "2.0")


    # REPRAP COMPATIBILITY
    if "REPRAPCOMPATIBLE" in line:
        v.reprap_compatible = True
        return

    # Program parameters
    if "NOGUI" in line:
        v.gui = False
        return

    if "CONSOLEWAIT" in line:
        v.consolewait = True

    if "IGNOREWARNINGS" in line:
        v.ignore_warnings = True

    if "ABSOLUTEEXTRUDER" in line:
        v.absolute_extruder = True
        app.log.info("Convert to absolute extrusion parameters")