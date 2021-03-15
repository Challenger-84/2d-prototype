# Importing Dependencies
import arcade
import random
from objects.platform import Platform

"""Procedural Generation"""


class ChunkMarker(arcade.SpriteSolidColor):

    def __init__(self, x, y, width, height, chunk):
        super().__init__(width, height, arcade.color.RED)
        self.chunk = chunk

        # Setting the position
        self.left = x
        self.bottom = y

    def on_update(self, delta_time: float = 1 / 60):
        self.left = self.chunk.start_x


# Chunk Class
class Chunk:
    """The Chunk Class"""

    def __init__(self, start_x, length, entry_points: list,
                 platform_list: arcade.SpriteList, screen: arcade.Window):

        self.start_x = start_x
        self.length = length
        self.entry_points = entry_points
        self.platform_SpriteList = platform_list
        self.screen = screen

        self.end_platforms = []
        self.in_platforms = []
        self.platform_width = 50
        self.color = random.choice([arcade.color.WHITE])
        self.collide_resistance = 1

        # Spawning Platforms in the chunk
        self.generate_platforms()

    @property
    def end_x(self):
        return self.start_x + self.length

    @property
    def platform_ends(self):
        if self.end_platforms:
            return [(platform.right, platform.bottom) for platform in self.end_platforms]
        else:
            return self.entry_points

    def y_to_spawn_platform(self, entry_y, max_offset_y):
        """This function decides which y level to spawn the next platform
            Above, Below or same level"""
        offset_y = random.randrange(20, max_offset_y)  # Offset of y from the previous platform
        higher_y = entry_y + offset_y
        lower_y = entry_y - offset_y

        y_level = random.randint(1, 3)

        if y_level == 1:  # Spawn Above the current y
            if higher_y < self.screen.height - self.platform_width - 100:
                return higher_y
            else:
                return self.y_to_spawn_platform(entry_y, max_offset_y)

        if y_level == 2:  # Spawn Below the current y
            if lower_y >= 0:
                return lower_y
            else:
                return self.y_to_spawn_platform(entry_y, max_offset_y)

        if y_level == 3:  # Spawn on same level
            return entry_y

    def random_length_generator(self, min_val, entry_x):
        try:
            if self.end_x - entry_x > 500:
                return random.randrange(min_val, 500)
            else:
                return random.randrange(min_val, int(self.end_x - entry_x))
        except ValueError:
            return None

    def x_to_spawn_platform(self, entry_x, prev_was_air=False):
        """This function decides on which x co-ordinate to spawn
            the platform on or to not spawn the platform"""

        is_air = random.randint(0, 1)

        if is_air and not prev_was_air:
            # Not spawning any platform
            air_length = random.randrange(50, 200)
            return self.x_to_spawn_platform(entry_x + air_length, prev_was_air=True)

        else:
            # If platform should be spawned
            platform_length = self.random_length_generator(100, entry_x)  # The length can be from 50 to till chunk end
            if platform_length:
                if self.end_x - (entry_x + platform_length) < 50:
                    platform_length += int(self.end_x - (entry_x + platform_length))
                return entry_x, platform_length
            else:
                return None

    def spawn_platform(self, x, y, offset_y, offset_x=0, platform: Platform = None):

        platform_y = self.y_to_spawn_platform(y, offset_y)
        if not offset_x:
            platform_xlength = self.x_to_spawn_platform(x)
        else:
            platform_xlength = self.x_to_spawn_platform(random.randrange(int(x), int(offset_x)))

        if platform_xlength:  # If the platform can spawn
            platform_x, platform_length = platform_xlength
            platform = Platform(platform_x, platform_y, platform_length, 50, self.color)

            # Check if the platform collides with another platform
            if platform.collides_with_list(self.platform_SpriteList):
                print('collides')
                self.collide_resistance -= 0.1  # Lessen the value of collide resistance
                if self.collide_resistance < random.random():
                    # There is a chance the no new platform will be spawned if there is a lot of collision
                    self.spawn_platform(x, y, offset_y, offset_x)  # If it can create a new platform
                    self.collide_resistance -= 0
                del platform  # delete this platform
            else:
                self.platform_SpriteList.append(platform)

                if self.end_x - (platform_x + platform_length) > 150:  # If the platform in not near the end
                    self.in_platforms.append(platform)  # Add it to the in platforms list

                else:    # If the platform is at the end
                    self.end_platforms.append(platform)  # Add it to the end platforms list
        else:
            if platform:
                if platform not in self.end_platforms:
                    self.end_platforms.append(platform)

    def generate_platforms(self):
        """Called whenever a chunk is created
            to generate platforms inside the chunk"""

        # 1 in 10 chance to spawn a new random platform out of nowhere
        if len(self.entry_points) < 2:
            new_platform_chance = random.randint(0, 4)
        else:
            new_platform_chance = random.randint(0, 49)

        print(new_platform_chance)
        if new_platform_chance == 0:
            # Spawn a random platform
            self.spawn_platform(self.start_x, random.randrange(0, self.screen.height - 50),
                                offset_y=200, offset_x=self.end_x - 150)

            # Spawn platforms for each entry point
        for entry_point in self.entry_points:
            self.spawn_platform(entry_point[0], entry_point[1],
                                offset_y=200)

        # print(f'before {len(self.in_platforms)}')

        # Platforms inside the chunk go through this for loop
        # This list extends as the for loop continues because it adds new platforms to the list
        # When it generates a platform at the end of the chunk it stops
        for platform in self.in_platforms:
            entry_y = platform.bottom
            offset_y = 200
            entry_x = platform.right

            self.spawn_platform(entry_x, entry_y, 200, platform=platform)

        for platform in self.end_platforms:
            if platform in self.in_platforms:
                self.in_platforms.remove(platform)

        # print(f'after {len(self.in_platforms)}')
        # print(f'ends {len(self.end_platforms)}')


def max_x(platform_end):
    return platform_end[0]


class LevelGenerator:

    def __init__(self, platform_list: arcade.SpriteList,
                 chunk_marker_list: arcade.SpriteList, screen: arcade.Window):
        self.platform_list = platform_list
        self.chunk_marker_list = chunk_marker_list
        self.screen = screen

        self.chunks = []

        # Generate first platform
        initial_platform = Platform(0, 200, 1000, 50, arcade.color.WHITE)
        self.platform_list.append(initial_platform)

        # Generating the first chunk
        self.generate_first_chunk(initial_platform)

    def generate_first_chunk(self, initial_platform):
        """This is called when initializing to
            generate the first platform"""
        start_x = initial_platform.right
        endpoint = [(initial_platform.right, initial_platform.bottom)]
        chunk = Chunk(start_x, random.randrange(1000, 2000), endpoint, self.platform_list, self.screen)

        chunk_marker = ChunkMarker(chunk.start_x, 0, 5, 650, chunk)
        self.chunk_marker_list.append(chunk_marker)

        # Appending to the chunk list
        # self.chunks = np.append(self.chunks, chunk)
        self.chunks.append(chunk)

    def generate_new_chunk(self):
        # Generate a new chunk
        prev_chunk = self.chunks[-1]  # Getting the last chunk

        length_of_chunk = random.randrange(1000, 2000, 10)
        platforms_ends = sorted(prev_chunk.platform_ends, key=max_x, reverse=True)
        start_x = prev_chunk.end_x

        # print('chunk end: ' + str(prev_chunk.end_x))
        # print('platform end ' + str(platforms_ends[0][0]))

        new_chunk = Chunk(start_x, length_of_chunk, platforms_ends, self.platform_list, self.screen)
        chunk_marker = ChunkMarker(new_chunk.start_x, 0, 5, 650, new_chunk)

        self.chunks.append(new_chunk)
        # self.chunks = np.append(self.chunks, new_chunk)  # Append to the array
        self.chunk_marker_list.append(chunk_marker)

    def update(self, player_x, scroll, delta_time):
        # Called every frame
        last_chunk = self.chunks[-1]

        if last_chunk.end_x - player_x < 2000:
            self.generate_new_chunk()

        # Adding scroll to chunk and deleting them if outside the screen
        chunks_to_del = []

        for chunk in self.chunks:
            chunk.start_x -= scroll * delta_time
            if chunk.end_x < -scroll * delta_time:
                chunks_to_del.append(chunk)

        for chunk in chunks_to_del:
            # index = np.where(self.chunks == chunk)
            self.chunks.remove(chunk)
            del chunk
