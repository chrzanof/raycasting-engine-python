import math

from commands.ChangeWeaponCommand import ChangeWeaponCommand
from commands.MoveActorCommand import MoveActorCommand
from commands.RotateActorCommand import RotateActorCommand
from commands.ZoomCommand import ZoomCommand
from settings import *


class InputHandler:
    """class for handling input from keyboard"""

    def __init__(self, window, actor):
        self.window = window
        self.input_buffer = []
        self.window.bind("<KeyPress>", self.keydown)
        self.window.bind("<KeyRelease>", self.keyup)
        self.actor = actor

    def keyup(self, e):
        """
        detects key being released and removes it from input_buffer
        :param e: event
        """
        if e.keysym in self.input_buffer:
            self.input_buffer.pop(self.input_buffer.index(e.keysym))

    def keydown(self, e):
        """
        detects key being pressed and adds it to input_buffer
        :param e: event
        """
        if e.keysym not in self.input_buffer:
            self.input_buffer.append(e.keysym)

    def handle_input(self):
        """
        this method checks which key is present in input_buffer and returns command_buffer array that contains command
         objects
        :return: command buffer
        """
        dpx = self.actor.speed * math.cos(self.actor.angle)
        dpy = self.actor.speed * math.sin(self.actor.angle)
        dpx90 = self.actor.speed * math.cos(self.actor.angle + 0.5 * math.pi)
        dpy90 = self.actor.speed * math.sin(self.actor.angle + 0.5 * math.pi)
        command_buffer = []
        if KEY_MOVE_UP in self.input_buffer:
            command_buffer.append(MoveActorCommand(self.actor, dpx, dpy))
        if KEY_MOVE_LEFT in self.input_buffer:
            command_buffer.append(MoveActorCommand(self.actor, -dpx90, -dpy90))
        if KEY_MOVE_DOWN in self.input_buffer:
            command_buffer.append(MoveActorCommand(self.actor, -dpx, -dpy))
        if KEY_MOVE_RIGHT in self.input_buffer:
            command_buffer.append(MoveActorCommand(self.actor, dpx90, dpy90))
        if KEY_ROTATE_LEFT1 in self.input_buffer:
            command_buffer.append(RotateActorCommand(self.actor, -self.actor.rotation_speed))
        if KEY_ROTATE_RIGHT1 in self.input_buffer:
            command_buffer.append(RotateActorCommand(self.actor, self.actor.rotation_speed))
        if KEY_ROTATE_LEFT2 in self.input_buffer:
            command_buffer.append(RotateActorCommand(self.actor, -self.actor.rotation_speed))
        if KEY_ROTATE_RIGHT2 in self.input_buffer:
            command_buffer.append(RotateActorCommand(self.actor, self.actor.rotation_speed))
        if KEY_ZOOM_IN in self.input_buffer:
            command_buffer.append(ZoomCommand(self.actor, -0.01))

        if KEY_ZOOM_OUT in self.input_buffer:
            command_buffer.append(ZoomCommand(self.actor, 0.01))

        if KEY_WEAPON_1 in self.input_buffer:
            command_buffer.append(ChangeWeaponCommand(self.actor, 0))
        if KEY_WEAPON_2 in self.input_buffer:
            command_buffer.append(ChangeWeaponCommand(self.actor, 1))
        if KEY_WEAPON_3 in self.input_buffer:
            command_buffer.append(ChangeWeaponCommand(self.actor, 2))

        return command_buffer
