# coding=utf-8
class Main():

    def __init__(self, p_timer, p_lcd, p_t):
        self.timer = p_timer
        self.lcd = p_lcd
        self.t = p_t

    def Set(self):
        self.lcd.display(self.t.toString())
        self.timer.start(1000)
        self.h = self.t.hour()
        self.m = self.t.minute()
        self.s = self.t.second()

    def Time(self):
        if self.s > 0:
            self.s -= 1
        else:
            if self.m > 0:
                self.m -= 1
                self.s = 59
            elif self.m == 0 and self.h > 0:
                self.h -= 1
                self.m = 59
                self.s = 59
            else:
                self.timer.stop()
        # time = ("{0}:{1}:{2}".format(self.h, self.m, self.s))
        time = ("{0}:{1}".format(self.m, self.s))

        self.lcd.setDigitCount(len(time))
        self.lcd.display(time)
