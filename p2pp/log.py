import sys

import p2pp.variables as v
import p2pp.colornames as colornames

class LogProviderBase:
    def log_error(self, message, color):
        print("Error: " + message, sys.stderr)

    def log_warning(self, message, color):
        print("Warning: " + message)

    def log_info(self, message, color):
        print(message)

class LogService:
    __service = None

    def __init__(self, service = LogProviderBase()):
        self.__service = service

    def register_service(self, service):
        self.__service = service

    def get_service(self):
        return self.__service

    def error(self, message = "", color = None):
        self.__service.log_error(message, color)

    def warning(self, message = "", color = None):
        self.__service.log_warning(message, color)

    def info(self, message = "", color = None):
        self.__service.log_info(message, color)

    def summary(self, summary):
        self.info("-" * 19, "blue")
        self.info("   Print Summary", "blue")
        self.info("-" * 19, "blue")
        self.info("")
        self.info("Number of splices:    {0:5}".format(len(v.splice_extruder_position)))
        self.info("Number of pings:      {0:5}".format(len(v.ping_extruder_position)))
        self.info("Total print length {:-8.2f}mm".format(v.total_material_extruded))
        self.info("")

        if v.full_purge_reduction or v.tower_delta:
            self.info("Tower Delta Range  {:.2f}mm -  {:.2f}mm".format(v.min_tower_delta, v.max_tower_delta))
            self.info("")
            self.info("Inputs/Materials used:")

        for i in range(len(v.palette_inputs_used)):
            if v.palette_inputs_used[i]:
                filament_used = v.material_extruded_per_color[i]
                filament_type = v.filament_type[i]
                filament_color = '#' + v.filament_color_code[i]
                filament_color_name = colornames.find_nearest_colour(filament_color)
                
                self.info("  \tInput  {} {:-8.2f}mm - {} \t[####]\t\t{}".format(i, filament_used, filament_type, filament_color_name), filament_color)

        self.info("")
        for line in summary:
            self.info(line[1:].strip(), "black")
        self.info("")