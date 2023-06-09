from SpriteRender import SpriteRender
from objects.TextureStripe import TextureStripe
from utils import *
from math import *

from settings import *


class RaycastingEngine:
    """class responsible for 3D (2.5D actually) view """
    def __init__(self, width, height, level, player, textures, sprites):
        self.width = width
        self.height = height
        self.level = level
        self.player = player
        self.textures = textures
        self.sprites = sprites

    def render(self, canvas):
        """
        rendering objects in the furthest to the nearest order
        :param canvas: canvas
        :return: canvas: updated canvas
        """
        canvas.create_rectangle(0, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, fill=rgb_to_hex(FLOOR_COLOR_RGB),
                                width=0)
        canvas.create_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT / 2, fill=rgb_to_hex(CEILING_COLOR_RGB), width=0)

        render_buffer = self.cast_rays()

        for sprite in self.sprites:
            screen_x, width, height, brightness, isVisible, distance = self.calculate_sprite_screen_parameters(sprite)
            params = (sprite,
                      isVisible,
                      (screen_x, self.height/2, width, height, brightness))
            sprite_render = SpriteRender(params)
            render_buffer.append((sprite_render, distance))

        render_buffer = sorted(render_buffer, key=lambda o: o[1], reverse=True)
        for obj in render_buffer:
            obj[0].render(canvas)

        return canvas

    def calculate_sprite_screen_parameters(self, sprite):
        """
        calculating all parameters necessary to render sprite on screen
        :param sprite:
        :return: screen x coordinate, width, height, brightness modifier, isVisible, distance to player
        """
        theta = math.atan2((sprite.y - self.player.y), (sprite.x - self.player.x))
        beta = self.player.angle - theta
        if beta < 0:
            beta = beta + 2 * math.pi
        if beta >= 2 * math.pi:
            beta = beta - 2 * math.pi

        isVisible = True
        if self.player.fov < beta < 2 * math.pi - self.player.fov:
            isVisible = False
        distance = sqrt((self.player.x - sprite.x) ** 2 + (self.player.y - sprite.y) ** 2)
        distance = distance * cos(beta)
        if distance < sprite.render_radius:
            isVisible = False
        brightness_scale = 1 - min(distance / self.player.vision_distance, 1)
        scale_h = 1 / (distance * tan(self.player.fov_vertical))
        height = SCREEN_HEIGHT * scale_h
        width = SCREEN_WIDTH * scale_h
        screen_dx = distance * tan(self.player.fov / 2) - distance * tan(beta)
        a = screen_dx / (2 * distance * tan(self.player.fov / 2))
        screen_position_x = LEVEL_SCREEN_MARGIN_LEFT + a * SCREEN_WIDTH

        return screen_position_x, int(width), int(height), brightness_scale, isVisible, distance

    def cast_rays(self):
        """
        method performing a ray casting algorithm
        :return: array of textured stripes
        """
        texture_stripes = []
        ra = self.player.angle - self.player.fov / 2
        dra = self.player.fov / NUMBER_OF_RAYS

        for i in range(0, NUMBER_OF_RAYS):
            if ra < 0:
                ra = ra + 2 * math.pi
            if ra > 2 * math.pi:
                ra = ra - 2 * math.pi

            # horizontal check
            horizontal_ray_len, hit_point_xh, hit_point_yh, texture_index_h = self.check_ray_collision(ra,
                                                                                                       self.player.x,
                                                                                                       self.player.y,
                                                                                                       self.level
                                                                                                       .level_map)

            # vertical check
            ra_rotated = ra - radians(90)
            if ra_rotated < 0:
                ra_rotated = ra_rotated + 2 * pi
            if ra_rotated > 2 * pi:
                ra_rotated = ra_rotated - 2 * pi

            px_rotated, py_rotated = return_rotated_actor_position(self.player.x, self.player.y, -90,
                                                                   len(self.level.level_map),
                                                                   len(self.level.level_map[0]))
            vertical_rey_len, hit_point_xv, hit_point_yv, texture_index_v = self.check_ray_collision(ra_rotated,
                                                                                                     px_rotated,
                                                                                                     py_rotated,
                                                                                                     self.level.level_map_rotated)

            if horizontal_ray_len < vertical_rey_len:
                horizontal = True
                wall_color = rgb_to_hex(HORIZONTAL_WALL_COLOR_RGB)
                wall_dist = horizontal_ray_len
                hit_point_y = hit_point_yh
                texture_index = texture_index_h
            else:
                horizontal = False
                wall_color = rgb_to_hex(VERTICAL_WALL_COLOR_RGB)
                wall_dist = vertical_rey_len
                hit_point_y = hit_point_yv
                texture_index = texture_index_v

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
            screen_position_x = LEVEL_SCREEN_MARGIN_LEFT + a * SCREEN_WIDTH

            # calculating next ray position in order to fill the gap
            next_screen_position_x = screen_position_x
            if i < NUMBER_OF_RAYS:
                screen_dx_next = wall_dist * tan(self.player.fov / 2) - wall_dist * tan(ca - dra)
                a_next = screen_dx_next / (2 * wall_dist * tan(self.player.fov / 2))
                next_screen_position_x = LEVEL_SCREEN_MARGIN_LEFT + a_next * SCREEN_WIDTH

            #  drawing line
            scale_dist = int(max(0.5 * wall_dist, 1))
            color_scale_dist = 1 - min(wall_dist / self.player.vision_distance, 1)
            texture = self.textures.get(texture_index)
            if not horizontal:
                if ra > math.radians(180):
                    texture_array = texture.rgb_array_reversed
                else:
                    texture_array = texture.rgb_array
            else:
                if math.radians(270) > ra > math.radians(90):
                    texture_array = texture.rgb_array_reversed
                else:
                    texture_array = texture.rgb_array
            texture_col = int(abs((hit_point_y - int(hit_point_y))) * len(texture_array))

            segments_list = []
            # with textures
            if wall_dist < self.player.vision_distance and RENDER_TEXTURES:
                for i in range(0, len(texture.rgb_array), scale_dist):
                    r = int(texture_array[i][texture_col][0] * color_scale_dist)
                    g = int(texture_array[i][texture_col][1] * color_scale_dist)
                    b = int(texture_array[i][texture_col][2] * color_scale_dist)
                    color = rgb_to_hex((r, g, b))

                    segment = (screen_position_x,
                               LEVEL_SCREEN_MARGIN_TOP + SCREEN_HEIGHT / 2 - 0.5 * line_height + i * line_height / len(
                                   texture.rgb_array),
                               next_screen_position_x,
                               LEVEL_SCREEN_MARGIN_TOP + SCREEN_HEIGHT / 2 - 0.5 * line_height + (
                                           i + scale_dist) * line_height / len(texture.rgb_array),
                               color,
                               0)
                    segments_list.append(segment)

            else:
                r, g, b = hex_to_rgb(wall_color)
                r = int(r * color_scale_dist)
                g = int(g * color_scale_dist)
                b = int(b * color_scale_dist)
                wall_color = rgb_to_hex((r, g, b))

                segment = (screen_position_x,
                           LEVEL_SCREEN_MARGIN_TOP + SCREEN_HEIGHT / 2 - 0.5 * line_height,
                           next_screen_position_x,
                           LEVEL_SCREEN_MARGIN_TOP + SCREEN_HEIGHT / 2 + 0.5 * line_height,
                           wall_color,
                           0)
                segments_list.append(segment)

            texture_stripe = TextureStripe(segments_list)
            texture_stripes.append((texture_stripe, wall_dist, True))
            ra = ra + dra
        return texture_stripes

    def check_ray_collision(self, ray_angle, player_x, player_y, level):
        """
        casting a single ray
        :param ray_angle: angle of the ray relative to the world
        :param player_x: player x coordinate
        :param player_y: player y coordinate
        :param level: level matrix - zeros represents empty space, any number higher than 0 is a texture id
        :return: ray length, wall hit-point x coordinate, wall hit-point y coordinate, index of texture
        """
        reverse = 0
        step = 0
        ray_dx = 0
        ray_dy = 0
        texture_index = 0
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
                        texture_index = level[int(player_y + ray_dy - reverse)][int(player_x + ray_dx - reverse)]
                        break
                else:
                    break
                ray_dx += step
        else:
            ray_length = inf
        hit_point_x = player_x + ray_dx
        hit_point_y = player_y + ray_dy
        return ray_length, hit_point_x, hit_point_y, texture_index
