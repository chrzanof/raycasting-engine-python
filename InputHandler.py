import math

from commands.MoveActorCommand import MoveActorCommand
from commands.RotateActorCommand import RotateActorCommand


class InputHandler:

    def __init__(self, window, actor):
        self.window = window
        self.input_buffer = []
        self.window.bind("<KeyPress>", self.keydown)
        self.window.bind("<KeyRelease>", self.keyup)
        self.actor = actor

    def keyup(self, e):
        if e.keysym in self.input_buffer:
            self.input_buffer.pop(self.input_buffer.index(e.keysym))

    def keydown(self, e):
        if e.keysym not in self.input_buffer:
            self.input_buffer.append(e.keysym)

    def handle_input(self):
        dpx = self.actor.speed * math.cos(self.actor.angle)
        dpy = self.actor.speed * math.sin(self.actor.angle)
        dpx90 = self.actor.speed * math.cos(self.actor.angle + 0.5 * math.pi)
        dpy90 = self.actor.speed * math.sin(self.actor.angle + 0.5 * math.pi)
        command_buffer = []
        if 'w' in self.input_buffer:
            command_buffer.append(MoveActorCommand(self.actor, dpx, dpy))
        if 'a' in self.input_buffer:
            command_buffer.append(MoveActorCommand(self.actor, -dpx90, -dpy90))
        if 's' in self.input_buffer:
            command_buffer.append(MoveActorCommand(self.actor, -dpx, -dpy))
        if 'd' in self.input_buffer:
            command_buffer.append(MoveActorCommand(self.actor, dpx90, dpy90))
        if 'Left' in self.input_buffer:
            command_buffer.append(RotateActorCommand(self.actor, -self.actor.rotation_speed))
        if 'Right' in self.input_buffer:
            command_buffer.append(RotateActorCommand(self.actor, self.actor.rotation_speed))
        if 'q' in self.input_buffer:
            command_buffer.append(RotateActorCommand(self.actor, -self.actor.rotation_speed))
        if 'e' in self.input_buffer:
            command_buffer.append(RotateActorCommand(self.actor, self.actor.rotation_speed))

        return command_buffer
