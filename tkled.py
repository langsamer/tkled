import tkinter as tk
from tkinter.messagebox import showerror
from backend import Blinker, Eventer
from broker import Broker

LED_RED_ON_IMG = './resources/led_red_on.gif'
LED_RED_OFF_IMG = './resources/led_red_off.gif'
LED_GREEN_ON_IMG = './resources/led_green_on.gif'
LED_GREEN_OFF_IMG = './resources/led_green_off.gif'


class Application(tk.Frame):
    def __init__(self, master=None, queue=None):
        super().__init__(master)
        self._create_widgets(master)
        self._mq = Broker(event_generate=master.event_generate)
        master.bind('<<SENT_EVENT>>', self.handle_event)

    def _create_widgets(self, master):
        self.mainframe = tk.Frame(master)
        self.mainframe.grid(row=1, column=1, sticky='NESW')
        b = tk.Button(self.mainframe, text="a button")
        b.configure(command=self.button_command)
        # b.configure(command=lambda: self.button_command(b))
        b.grid(row=1, column=1, sticky='NEW')
        self.red_led = Indicator(master, LED_RED_OFF_IMG, LED_RED_ON_IMG, 100)
        self.red_led.grid(row=2, column=1, sticky='SE')
        self.red_blinker = Blinker(self.after, indfunc=self.red_led.flash)
        self.green_led = Indicator(master, LED_GREEN_OFF_IMG, LED_GREEN_ON_IMG, 250)
        self.green_led.grid(row=2, column=2, sticky='SW')
        self.info_widget = tk.Label(master, text="<empty>")
        self.info_widget.grid(row=3, column=1, sticky='SEW')

    def button_command(self):
        self.red_blinker.action()
        self.green_led.blink()
        x = Eventer(after=self.after,
                    indicate_func=self._mq.write)
        x.action()

    def handle_event(self, e):
        print(str(self._mq))
        try:
            name, data = self._mq.read()
        except IndexError:
            return
        if name == 'Info':
            self.info_widget.config(text=data)
        elif name == 'Alert':
            showerror('Error', "{!s}".format(data))


class Indicator(tk.Label):
    def __init__(self, master,
                 low_image=LED_RED_OFF_IMG, high_image=LED_RED_ON_IMG,
                 low_duration=500, high_duration=500,
                 ):
        self.led_img = (tk.PhotoImage(file=low_image), tk.PhotoImage(file=high_image))
        self.duration = (low_duration, high_duration)
        self.job_id = None
        self.is_on = 0
        self.toggle = None
        super().__init__(master, image=self.led_img[self.is_on])

    def switch_on(self):
        """Switch to 'high' indication"""
        if self.job_id:
            self.after_cancel(self.job_id)
            self.job_id = None
        self.config(image=self.led_img[1])

    def switch_off(self):
        """Switch to 'low' indication"""
        if self.job_id:
            self.after_cancel(self.job_id)
            self.job_id = None
        self.config(image=self.led_img[0])

    def flash(self):
        """Switch to 'high' indication only for a brief moment"""
        self.switch_on()
        self.job_id = self.after(self.duration[1], self.switch_off)

    def blink(self):
        """Switch on blinking, ie. continuous toggle between on and off."""
        if not self.toggle:
            self.toggle = self._toggle
        self.toggle()

    def _toggle(self):
        self.is_on = not self.is_on
        self.job_id = self.after(self.duration[self.is_on], self.toggle)
        self.config(image=self.led_img[self.is_on])


if __name__ == '__main__':
    tkroot = tk.Tk()
    app = Application(tkroot)
    app.mainloop()
