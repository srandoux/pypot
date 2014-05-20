import time
import threading
import pygame.midi


from collections import deque, namedtuple


MidiEvent = namedtuple('MidiEvent',
                       ('status', 'data1', 'data2', 'data3', 'timestamp'))


class MidiSensor(threading.Thread):
    def __init__(self, input_id, freq=10., chunk=10):
        threading.Thread.__init__(self)
        pygame.midi.init()

        self.midi_controller = pygame.midi.Input(input_id)
        self.running = threading.Event()
        self.dt = 1.0 / freq
        self.chunk = chunk

        self.events = deque()

    def stop(self):
        self.running.clear()

    def run(self):
        while self.running.is_set():
            if self.controller.poll():
                data = self.controller.read(self.chunk)
                events = [MidiEvent(status, data1, data2, data3, timestamp)
                          for ((status, data1, data2, data3), timestamp) in data]

                self.events.extend(events)

            time.sleep(self.dt)
