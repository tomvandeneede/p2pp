__author__ = 'Tom Van den Eede'
__copyright__ = 'Copyright 2018-2019, Palette2 Splicer Post Processing Project'
__credits__ = ['Tom Van den Eede',
               'Tim Brookman'
               ]
__license__ = 'GPLv3'
__maintainer__ = 'Tom Van den Eede'
__email__ = 'P2PP@pandora.be'

try:
    # p ython version 2.x
    import Tkinter as tkinter
    import ttk
    import tkMessageBox
except ImportError:
    # python version 3.x
    import tkinter
    from tkinter import ttk
    from tkinter import messagebox as tkMessageBox

import os
import sys
from platform import system
from os.path import dirname, abspath

import p2pp.colornames as colornames
import p2pp.variables as v
import version
from p2pp.log import LogProviderBase

boldfontlarge = 'Helvetica 30 bold'
normalfont = 'Helvetica 16'
boldfont = 'Helvetica 16 bold'
fixedfont = 'Courier 14'
fixedsmallfont = 'Courier 12'

class Gui(LogProviderBase):
    last_pct = None
    color_count = None

    mainwindow = None
    progress = None
    loglist = None
    closebuttron = None
    progressbar = None
    infosubframe = None
    printerid = None
    filename = None
    logoimage = None

    def __init__(self):
        self.last_pct = -1
        self.color_count = 0

        self.mainwindow = tkinter.Tk()
        self.mainwindow.title("Palette2 Post Processing for PrusaSliceer")
        self.__center(self.mainwindow, 800, 600)

        if system() == 'Windows':
            logo_image = os.path.dirname(sys.argv[0]) + '\\favicon.ico'
            self.mainwindow.iconbitmap(logo_image)
            self.mainwindow.update()

        self.mainwindow['padx'] = 10
        self.mainwindow['pady'] = 10

        # Top Information Frqme
        self.infoframe = tkinter.Frame(self.mainwindow, border=3, relief='sunken', background="#808080")
        self.infoframe.pack(side=tkinter.TOP, fill=tkinter.X)

        # logo
        base_path = dirname(dirname(abspath(__file__)))
        self.logoimage = tkinter.PhotoImage(file=base_path + "/appicon.ppm")
        logofield = tkinter.Label(self.infoframe, image=self.logoimage)
        logofield.pack(side=tkinter.LEFT, fill=tkinter.Y)

        self.infosubframe = tkinter.Frame(self.infoframe, background="#808080")
        self.infosubframe.pack(side=tkinter.LEFT, fill=tkinter.X)
        self.infosubframe["padx"] = 20

        # file name display
        tkinter.Label(self.infosubframe, text='Filename:', font=boldfont, background="#808080").grid(row=0, column=1, sticky="w")
        self.filename = tkinter.StringVar()
        self.setfilename("-----")
        tkinter.Label(self.infosubframe, textvariable=self.filename, font=normalfont, background="#808080").grid(row=0, column=2,
                                                                                                    sticky="w")
        # printer ID display
        self.printerid = tkinter.StringVar()
        self.set_printer_id("-----")

        tkinter.Label(self.infosubframe, text='Printer ID:', font=boldfont, background="#808080").grid(row=1, column=1, sticky="w")
        tkinter.Label(self.infosubframe, textvariable=self.printerid, font=normalfont, background="#808080").grid(row=1, column=2,
                                                                                                        sticky="w")

        tkinter.Label(self.infosubframe, text="P2PP Version:", font=boldfont, background="#808080").grid(row=2, column=1,
                                                                                                    sticky="w")
        tkinter.Label(self.infosubframe, text=version.Version, font=normalfont, background="#808080").grid(row=2, column=2,
                                                                                                    sticky="w")

        # progress bar
        self.progress = tkinter.IntVar()
        self.progress.set(0)
        tkinter.Label(self.infosubframe, text='Progress:', font=boldfont, background="#808080").grid(row=3, column=1, sticky="w")
        self.progressbar = ttk.Progressbar(self.infosubframe ,orient='horizontal', mode='determinate', length=500, maximum=100, variable=self.progress)
        self.progressbar.grid(row=3, column=2,  sticky='ew')

        # Log frame
        logframe = tkinter.Frame(self.mainwindow, border=3, relief="sunken")
        logframe.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        loglistscroll = tkinter.Scrollbar(logframe, orient=tkinter.VERTICAL)
        loglistscroll.pack(side='right', fill=tkinter.Y)

        self.loglist = tkinter.Text(logframe, yscrollcommand=loglistscroll.set, font=fixedsmallfont)
        self.loglist.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)

        loglistscroll.config(command=self.loglist.yview)

        # Button frame
        buttonframe = tkinter.Frame(self.mainwindow, border=1, relief="sunken")
        buttonframe.pack(side=tkinter.BOTTOM, fill=tkinter.X)

        self.closebutton = tkinter.Button(buttonframe, text="Exit", state=tkinter.DISABLED, command=self.close_window)
        self.closebutton.pack(side=tkinter.RIGHT, fill=tkinter.X, expand=1)

        self.mainwindow.rowconfigure(0, weight=1)
        self.mainwindow.rowconfigure(1, weight=1000)
        self.mainwindow.rowconfigure(2, weight=1)

        self.mainwindow.lift()
        self.mainwindow.attributes('-topmost', True)
        self.mainwindow.after_idle(self.mainwindow.attributes, '-topmost', False)
        self.mainwindow.update()

    def progress_string(self, pct):
        if self.last_pct == pct:
            return
        if pct == 100:
            if len(v.process_warnings) == 0:
                self.completed("  COMPLETED OK", '#008000')
            else:
                self.completed("  COMPLETED WITH WARNINGS",'#800000')
        else:
            self.progress.set(pct)
            self.mainwindow.update()
            self.last_pct = pct

    def completed(self, text, color):
        self.progressbar.destroy()
        progress_field = tkinter.Label(self.infosubframe , text=text, font=boldfont, foreground=color,  background="#808080")
        progress_field.grid(row=3, column=2, sticky="ew")

    def close_window(self):
        self.mainwindow.destroy()

    def update_button_pressed(self):
        v.upgradeprocess(version.latest_stable_version , v.update_file_list)
 
    def close_button_enable(self):
        self.closebutton.config(state=tkinter.NORMAL)
        # WIP disable upgrade for now
        # if not (v.upgradeprocess == None):
        #     tkinter.Button(buttonframe, text='Upgrade to '+version.latest_stable_version, command=update_button_pressed).pack(side=tkinter.RIGHT)
        self.mainwindow.mainloop()

    def __center(self, win, width, height):
        win.update_idletasks()
        x = (win.winfo_screenwidth() // 2) - (width // 2)  # center horizontally in screen
        y = (win.winfo_screenheight() // 2) - (height // 2)  # center vertically in screen
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        win.minsize(width, height)
        win.maxsize(width, height)

    def set_printer_id(self, text):
        self.printerid.set(text)
        self.mainwindow.update()

    def setfilename(self, text):
        self.filename.set(text)
        self.mainwindow.update()

    def user_error(self, header, body_text):
        tkMessageBox.showinfo(header, body_text)

    def ask_yes_no(self, title, message):
        return (tkMessageBox.askquestion(title, message).upper()=="YES")

    def configinfo(self):
        self.infosubframe.destroy()
        self.infosubframe = tkinter.Frame(self.infoframe, border=3, relief='sunken', background="#909090")
        self.infosubframe.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        tkinter.Label(self.infosubframe, text='CONFIGURATION  INFO', font=boldfontlarge, background="#909090").pack(side=tkinter.TOP, expand=1)
        tkinter.Label(self.infosubframe, text="P2PP Version "+version.Version+"\n", font=boldfont, background="#909090").pack( side=tkinter.BOTTOM)

    def __create_logitem(self, text, color="black", force_update=True, position=tkinter.END):
        text = text.strip()
        self.color_count += 1
        tagname = "color"+str(self.color_count)
        self.loglist.tag_configure(tagname, foreground=color)
        self.loglist.insert(position, "  " + text + "\n", tagname)
        if force_update:
            self.mainwindow.update()

    def log_info(self, message, color):
        self.__create_logitem(message, color)

    def log_warning(self, message, color):
        v.process_warnings.append(";" + message)
        self.__create_logitem(message, "red")

    def log_error(self, message, color):
        v.process_warnings.append(";" + message)
        self.__create_logitem(message, "red")