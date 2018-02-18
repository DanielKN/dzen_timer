import socket
import threading
import queue
import time

start_timer_pomodoro_button = "^ca(1, python time_client.py start1500) S ^ca()"
start_timer_break_button = "^ca(1, python time_client.py start300) B ^ca()"
pause_button = "^ca(1, python time_client.py pause) P ^ca()"
resume_button = "^ca(1, python time_client.py resume) R ^ca()"

# How often the timer will update
TIMER_PRECISION = .3


pause_input = queue.Queue(0)
resume_input = queue.Queue(0)
set_time_input = queue.Queue(0)


class CountdownTimer(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.set_time = 0
        self.paused = False
        self.time_started = 0


    def run(self):
        while True:
            time.sleep(TIMER_PRECISION)
            self.manage_status()
            self.generate_dzen_timer_string()


    def manage_status(self):

        set_time= self.get_queue_object(set_time_input, None)
        if set_time:
            self.set_time = set_time
            self.paused = False
            self.time_started = time.time()

        elif self.get_queue_object(pause_input, None):
            self.paused = True
            self.set_time = self.time_remaining

        elif self.get_queue_object(resume_input, None):
            self.paused = False
            self.time_started = time.time()

        elif self.time_remaining <= 0:
            self.set_time = 0
            self.paused = False

    def generate_dzen_timer_string(self):

        if self.paused:
            print("{} {} {} {}".format(
                start_timer_pomodoro_button,
                start_timer_break_button,
                resume_button,
                self.format_time(self.set_time)))


        elif self.set_time:
            print("{} {} {} {}".format(
                start_timer_pomodoro_button,
                start_timer_break_button,
                pause_button,
                self.format_time(self.time_remaining)))

        else:
            print("{} {} {} {}".format(
                start_timer_pomodoro_button,
                start_timer_break_button,
                pause_button,
                self.format_time(0)))

    def get_queue_object(self, queue_obj, return_value):
        try:
            return queue_obj.get(False)
        except queue.Empty:
            return return_value

    @property
    def time_remaining(self):
        return self.set_time - self.time_elapsed()


    def time_elapsed(self):
        return time.time() - self.time_started


    def format_time(self, elap):
        minutes = int(elap / 60)
        seconds = int(elap - minutes * 60.0)
        return '%02d:%02d' % (minutes, seconds)


class TimerInterface:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.timer = CountdownTimer()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,0)

        self.socket.bind((self.host, self.port))

    def run(self):
        self.timer.start()
        self.socket.listen(1)

        while True:
            conn, address = self.socket.accept()

            while True:
               data = conn.recv(1024)
               if data:
                   self.handle_input_data(data)
                   conn.close()
                   break

        self.socket.close()

    def handle_input_data(self, data):

        data = data.decode('utf-8')

        if data.startswith('start'):
           self.set_time(int(data[5:]))

        if data == 'pause':
           self.pause()

        if data == 'resume':
           self.resume()


    def set_time(self, t):
        if set_time_input.empty():
            set_time_input.put(t)

    def pause(self):
        if pause_input.empty():
            pause_input.put(True)

    def resume(self):
        if resume_input.empty():
            resume_input.put(True)




if __name__ == "__main__":
    timer_interface = TimerInterface('localhost', 49152)
    timer_interface.run()
