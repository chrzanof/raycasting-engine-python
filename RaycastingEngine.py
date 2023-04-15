from utils import *
from math import *

from settings import *


class RaycastingEngine:
    def __init__(self, width, height, level, player, textures):
        self.width = width
        self.height = height
        self.level = level
        self.player = player
        self.textures = textures

    def render(self, canvas):
        canvas.create_rectangle(0, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, fill=rgb_to_hex(FLOOR_COLOR_RGB),
                                width=0)
        canvas.create_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT / 2, fill=rgb_to_hex(CEILING_COLOR_RGB), width=0)
        self.cast_rays(canvas)
        return canvas

    def cast_rays(self, canvas):
        ra = self.player.angle - self.player.fov / 2
        dra = self.player.fov / NUMBER_OF_RAYS

        for i in range(0, NUMBER_OF_RAYS):
            if ra < 0:
                ra = ra + 2 * math.pi
            if ra > 2 * math.pi:
                ra = ra - 2 * math.pi

            # horizontal check - green ray
            horizontal_ray_len, hit_point_xh, hit_point_yh = self.check_ray_length(ra, self.player.x, self.player.y,
                                                                                   self.level.level_map)

            # vertical check -- yellow ray
            ra_rotated = ra - radians(90)
            if ra_rotated < 0:
                ra_rotated = ra_rotated + 2 * pi
            if ra_rotated > 2 * pi:
                ra_rotated = ra_rotated - 2 * pi

            px_rotated, py_rotated = return_rotated_actor_position(self.player.x, self.player.y, -90,
                                                                   len(self.level.level_map),
                                                                   len(self.level.level_map[0]))
            vertical_rey_len, hit_point_xv, hit_point_yv = self.check_ray_length(ra_rotated, px_rotated, py_rotated,
                                                                                 self.level.level_map_rotated)

            if horizontal_ray_len < vertical_rey_len:
                wall_color = rgb_to_hex(HORIZONTAL_WALL_COLOR_RGB)
                wall_dist = horizontal_ray_len
                hit_point_y = hit_point_yh
            else:
                wall_color = rgb_to_hex(VERTICAL_WALL_COLOR_RGB)
                wall_dist = vertical_rey_len
                hit_point_y = hit_point_yv

            # fish eye effect correction
            ca = self.player.angle - ra
            if ca < 0:
                ca += 2 * pi
            if ca >= 2 * pi:
                ca -= 2 * pi
            wall_dist = wall_dist * cos(ca)

            line_scale = 1 / (wall_dist * tan(self.player.fov_vertical))
            line_height = SCREEN_HEIGHT * line_scale

            # calculating ray position on the screen
            screen_dx = wall_dist * tan(self.player.fov / 2) - wall_dist * tan(ca)
            a = screen_dx / (2 * wall_dist * tan(self.player.fov / 2))

            # calculating next ray position in order to fill the gap
            screen_position_x = LEVEL_SCREEN_MARGIN_LEFT + a * SCREEN_WIDTH
            next_screen_position_x = screen_position_x
            if i < NUMBER_OF_RAYS:
                screen_dx_next = wall_dist * tan(self.player.fov / 2) - wall_dist * tan(ca - dra)
                a_next = screen_dx_next / (2 * wall_dist * tan(self.player.fov / 2))
                next_screen_position_x = LEVEL_SCREEN_MARGIN_LEFT + a_next * SCREEN_WIDTH

            color_scale_dist = 1 - min(wall_dist / self.player.vision_distance, 1)
            # r, g, b = hex_to_rgb(wall_color)
            # r = int(r * color_scale_dist)
            # g = int(g * color_scale_dist)
            # b = int(b * color_scale_dist)
            # wall_color = rgb_to_hex((r, g, b))

            # canvas.create_rectangle(screen_position_x,
            #                         LEVEL_SCREEN_MARGIN_TOP + SCREEN_HEIGHT / 2 - 0.5 * line_height,
            #                         next_screen_position_x,
            #                         LEVEL_SCREEN_MARGIN_TOP + SCREEN_HEIGHT / 2 + 0.5 * line_height,
            #                         fill=wall_color, width=0)
            texture_col = int((hit_point_y - int(hit_point_y)) * len(self.textures[0].rgb_array))

            for i in range(len(self.textures[0].rgb_array)):
                r = int(self.textures[0].rgb_array[i][texture_col][0] * color_scale_dist)
                g = int(self.textures[0].rgb_array[i][texture_col][1] * color_scale_dist)
                b = int(self.textures[0].rgb_array[i][texture_col][2] * color_scale_dist)
                color = rgb_to_hex((r, g, b))
                canvas.create_rectangle(
                    screen_position_x,
                    LEVEL_SCREEN_MARGIN_TOP + SCREEN_HEIGHT / 2 - 0.5 * line_height + i * line_height / len(
                        self.textures[0].rgb_array),
                    next_screen_position_x,
                    LEVEL_SCREEN_MARGIN_TOP + SCREEN_HEIGHT / 2 - 0.5 * line_height + (i + 1) * line_height / len(
                        self.textures[0].rgb_array),
                    fill=color, width=0
                )

            ra = ra + dra

    def check_ray_length(self, ray_angle, player_x, player_y, level):

        reverse = 0
        step = 0
        ray_dx = 0
        ray_dy = 0
        if 0 <= ray_angle < 0.5 * pi or 1.5 * pi < ray_angle <= 2 * pi:
            step = 1
        if 0.5 * pi < ray_angle < 1.5 * pi:
            step = -1

        if step != 0:
            if step == 1:
                ray_dx = math.ceil(player_x) - player_x
            elif step == -1:
                ray_dx = math.floor(player_x) - player_x
                reverse = 0.00001

            while True:
                ray_dy = ray_dx * tan(ray_angle)
                ray_length = sqrt(ray_dx ** 2 + ray_dy ** 2)
                max_x = len(level)
                if 0 < int((player_y + ray_dy)) < max_x:
                    if level[int(player_y + ray_dy - reverse)][int(player_x + ray_dx - reverse)] > 0:
                        break
                else:
                    break
                ray_dx += step
        else:
            ray_length = inf
        hit_point_x = player_x + ray_dx
        hit_point_y = player_y + ray_dy
        return ray_length, hit_point_x, hit_point_y
