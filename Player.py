import os
import time
import pygame
import numpy as np


class Player:

    def __init__(self, path='songs/dancing_queen'):

        track2file = {}
        for track in os.listdir(path):
            track_name = track.split('_')[0].lower()
            track2file[track_name] = os.path.join(os.getcwd(), path, track)

        print(track2file)

        pygame.mixer.init()
        self.channels = {}
        for track_name, file_path in track2file.items():
            self.channels[track_name] = pygame.mixer.Sound(file_path)
            self.channels[track_name].set_volume(1.0)

        self.playing = False
        self.config = {
            #          q0   q1   q2   q3   q4
            'vocals': [0.0, 0.0, 0.0, 0.4, 1.0],
            'bass': [1.0, 1.0, 1.0, 1.0, 1.0],
            'drums': [0.4, 0.4, 1.0, 1.0, 1.0],
            'other': [0.2, 1.0, 1.0, 1.0, 1.0],
        }
        self.n_bins = 5

    def play(self):
        if self.playing:
            return
        self.playing = True

        for name, channel in self.channels.items():
            channel.play()
            print(f'{name} volume {channel.get_volume()}')

    def stop(self):
        for name, channel in self.channels.items():
            channel.stop()

    def set_q(self, n: int, ms: int = 1000, n_intervals: int = 10):

        if not (0 <= n < self.n_bins):
            raise ValueError(f'n must be between 0 and {self.n_bins}')

        values = {
            name: np.linspace(start=channel.get_volume(), stop=self.config[name][n], num=n_intervals)
            for name, channel in self.channels.items()
        }

        print(values)

        interval = (ms / n_intervals) / 1000

        for i in range(n_intervals):
            for name, channel in self.channels.items():
                channel.set_volume(values[name][i])
            time.sleep(interval)
