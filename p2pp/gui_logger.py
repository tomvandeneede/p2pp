from p2pp.log import LogBase
import p2pp.gui as gui

class GuiLogProvider(LogBase):
    def log_error(self, message, color):
        gui.create_logitem(message, color)

    def log_warning(self, message, color):
        gui.log_warning(message)

    def log_info(self, message, color):
        print(message, color)