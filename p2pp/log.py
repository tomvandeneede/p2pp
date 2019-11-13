import sys

import p2pp.variables as v
import p2pp.colornames as colornames

class LogBase:
    def log_error(self, message):
        print("Error: " + message, sys.stderr)

    def log_warning(self, message):
        print("Warning: " + message)

    def log_info(self, message):
        print(message)

class LogService:
    __service = LogBase()

    def register_service(self, service):
        self.__service = service

    def get_service(self):
        return self.__service

    def error(self, message, color = None):
        self.__service.log_error(message)

    def warning(self, message, color = None):
        self.__service.log_warning(message)

    def info(self, message, color = None):
        self.__service.log_info(message)

    def summary(self, summary):
        self.info("-" * 19, "blue")
        self.info("   Print Summary", "blue")
        self.info("-" * 19, "blue")
        self.info("\n")
        self.info("Number of splices:    {0:5}".format(len(v.splice_extruder_position)))
        self.info("Number of pings:      {0:5}".format(len(v.ping_extruder_position)))
        self.info("Total print length {:-8.2f}mm".format(v.total_material_extruded))
        self.info("\n")

        if v.full_purge_reduction or v.tower_delta:
            self.info("Tower Delta Range  {:.2f}mm -  {:.2f}mm".format(v.min_tower_delta, v.max_tower_delta))
            self.info("\n")
            self.info("Inputs/Materials used:")

        for i in range(len(v.palette_inputs_used)):
            if v.palette_inputs_used[i]:
                filament_used = v.material_extruded_per_color[i]
                filament_type = v.filament_type[i]
                filament_color = colornames.find_nearest_colour('#' + v.filament_color_code[i])

                # TODO: build a standard color map and remap here instead of later
                color_tag_1 = i * 2
                color_tag_2 = i * 2 + 1
                
                self.info("  \tInput  {} {:-8.2f}mm - {} ".format(i, filament_used, filament_type), color_tag_1)
                self.info("  \t[####]\t", color_tag_2)
                self.info("  \t{}\n".format(filament_color), color_tag_1)

        self.info("\n")
        for line in summary:
            self.info(line[1:].strip(), "black")
        self.info("\n")