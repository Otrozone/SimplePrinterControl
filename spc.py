import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import tkinter.font as tkFont
import RPi.GPIO as GPIO
# import requests
from printerdata import printer_data
from config import conf
#import pdb

class Spc:
    def create_window(self):
        self.root.title("Simple printer control")
        width=780
        height=400
        self.offset=20
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        # root.resizable(width=False, height=False)

    def add_btn_light(self):
        btn_light=tk.Button(self.root)
        btn_light["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Tahoma', size=20)
        btn_light["font"] = ft
        btn_light["fg"] = "#000000"
        btn_light["justify"] = "center"
        btn_light["text"] = "Light"
        self.btn_light_image = tk.PhotoImage(file = r"./gfx/lightbulb-regular-small.png")
        btn_light["image"] = self.btn_light_image
        btn_light["compound"] = tk.LEFT
        btn_light.place(x=self.offset, y=self.offset, width=200, height=100)
        btn_light["command"] = self.btnLight_command

    def add_btn_print(self):
        btn_print=tk.Button(self.root)
        btn_print["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Tahoma', size=20)
        btn_print["font"] = ft
        btn_print["fg"] = "#000000"
        btn_print["justify"] = "center"
        btn_print["text"] = "Print"
        self.btn_print_image = tk.PhotoImage(file = r"./gfx/play-solid_36x48.png")
        btn_print["image"] = self.btn_print_image
        btn_print["compound"] = tk.LEFT
        btn_print.place(x=self.offset, y=100 + self.offset * 2, width=200, height=100)
        btn_print["command"] = self.btnPrint_command

    def add_btn_printer(self):
        btn_printer=tk.Button(self.root)
        btn_printer["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Tahoma', size=20)
        btn_printer["font"] = ft
        btn_printer["fg"] = "#000000"
        btn_printer["justify"] = "center"
        btn_printer["text"] = "Printer"
        self.btn_printer_image = tk.PhotoImage(file = r"./gfx/power-off-solid-small.png")
        btn_printer["image"] = self.btn_printer_image
        btn_printer["compound"] = tk.LEFT
        btn_printer.place(x=self.offset, y=220 + self.offset * 2, width=200, height=100)
        btn_printer["command"] = self.btnPrinter_command

    def get_top(self, section_name):
        if section_name not in self.section_counters:
            self.section_counters[section_name] = 1

        self.section_counters[section_name] += 1.5
        top_position = self.section_counters[section_name] * self.offset

        return top_position

    def add_status(self):
        ft = tkFont.Font(family='Tahoma', size=10)
        left = 200 + (2 * self.offset)

        self.state = tk.StringVar()
        self.state.set("Unknown")
        lbl_status = tk.Label(self.root, textvariable=self.state, relief=tk.FLAT, anchor="w", justify="left")
        lbl_status["font"] = ft
        lbl_status.place(x=left, y=self.offset, width=200, height=20)

        self.completion = tk.StringVar()
        self.completion.set("0")
        lbl_progress = tk.Label(self.root, textvariable=self.completion, relief=tk.FLAT, anchor="w", justify="left")
        lbl_progress["font"] = ft
        lbl_progress.place(x=left, y=self.get_top("mid"), width=200, height=20)

        self.completion_val = tk.DoubleVar()
        self.completion.set(0)
        self.pb_progress = ttk.Progressbar(self.root,orient='horizontal', variable=self.completion_val, length=100)
        self.pb_progress.place(x=left, y=self.get_top("mid"), width=200, height=20)

        self.print_time = tk.StringVar()
        self.print_time.set("0")
        lbl_print_time = tk.Label(self.root, textvariable=self.print_time, relief=tk.FLAT, anchor="w", justify="left")
        lbl_print_time["font"] = ft
        lbl_print_time.place(x=left, y=self.get_top("mid"), width=200, height=20)

        self.time_left = tk.StringVar()
        self.time_left.set("0")
        lbl_time_left = tk.Label(self.root, textvariable=self.time_left, relief=tk.FLAT, anchor="w", justify="left")
        lbl_time_left["font"] = ft
        lbl_time_left.place(x=left, y=self.get_top("mid"), width=200, height=20)

        self.filename = tk.StringVar()
        self.filename.set("0")
        lbl_file_name = tk.Label(self.root, textvariable=self.filename, anchor="w", justify="left")
        lbl_file_name["font"] = ft
        lbl_file_name.place(x=left, y=self.get_top("mid"), width=400, height=20)

    def seconds_to_hh_mm_ss(self, seconds):
        if seconds is not None:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return "-"

    def update(self):
        printer_data.update()

        self.state.set(f"Status: {printer_data.state}")
        self.print_time.set(f"Print time: {self.seconds_to_hh_mm_ss(printer_data.progress_print_time)}")
        self.time_left.set(f"Time left: {self.seconds_to_hh_mm_ss(printer_data.progress_time_left)}")
        self.completion_val.set(printer_data.progress_completion)
        self.completion.set(f"Progress: {printer_data.progress_completion}%")
        self.filename.set(f"Filename: {printer_data.filename}")

        self.root.after(1000, self.update)

    def __init__(self):
        self.section_counters = {}
        self.root = tk.Tk()

        self.create_window()
        self.add_btn_light()
        self.add_btn_print()
        self.add_btn_printer()
        self.add_status()

        self.update()
        
        #self.root.update()
        self.root.mainloop()

    def btnLight_command(self):
        print("Switching light")
        light_state = GPIO.input(conf.light_pin)
        GPIO.output(conf.light_pin, GPIO.LOW if light_state == 1 else GPIO.HIGH)

    def btnPrinter_command(self):
        result = messagebox.askyesno("Confirmation", "Are you sure that you want to switch the printer?")
        if result:
            print("Switching printer")
            printer_state = GPIO.input(conf.printer_pin)
            GPIO.output(conf.printer_pin, GPIO.LOW if printer_state == 1 else GPIO.HIGH)

    def btnPrint_command(self):
        printer_data.start()

if __name__ == "__main__":
    #pdb.set_trace()
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(conf.light_pin, GPIO.OUT)
    GPIO.setup(conf.printer_pin, GPIO.OUT)

    app = Spc()
