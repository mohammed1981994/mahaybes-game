import pygame
import random
import math
import sys
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.Sound.play(pygame.mixer.Sound(buffer=bytearray([i%256 for i in range(2000)])))
# Try to import Arabic text processing libraries
try:
    from arabic_reshaper import reshape
    from bidi.algorithm import get_display

    ARABIC_SUPPORT = True
    print("Arabic text processing libraries found!")
except ImportError:
    ARABIC_SUPPORT = False
    print("Arabic text processing libraries not found. Install with:")
    print("pip install arabic-reshaper python-bidi")
    print("Using fallback Arabic display method...")

# Constants
WIDTH, HEIGHT = 1200, 800
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
PINK = (255, 192, 203)
BLUE = (100, 149, 237)
GREEN = (144, 238, 144)
RED = (255, 99, 99)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
ORANGE = (255, 165, 0)
PURPLE = (138, 43, 226)
GOLD = (255, 215, 0)
DARK_BROWN = (101, 67, 33)

# Try to load Arabic font
try:
    # Try to load system Arabic fonts
    if sys.platform == "win32":
        ARABIC_FONT = pygame.font.Font("C:/Windows/Fonts/arial.ttf", 24)
        ARABIC_FONT_LARGE = pygame.font.Font("C:/Windows/Fonts/arial.ttf", 32)
        ARABIC_FONT_SMALL = pygame.font.Font("C:/Windows/Fonts/arial.ttf", 20)
    elif sys.platform == "darwin":  # macOS
        ARABIC_FONT = pygame.font.Font("/System/Library/Fonts/Arial.ttf", 24)
        ARABIC_FONT_LARGE = pygame.font.Font("/System/Library/Fonts/Arial.ttf", 32)
        ARABIC_FONT_SMALL = pygame.font.Font("/System/Library/Fonts/Arial.ttf", 20)
    else:  # Linux
        ARABIC_FONT = pygame.font.Font("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        ARABIC_FONT_LARGE = pygame.font.Font("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
        ARABIC_FONT_SMALL = pygame.font.Font("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
except:
    # Fallback to default font
    ARABIC_FONT = pygame.font.Font(None, 24)
    ARABIC_FONT_LARGE = pygame.font.Font(None, 32)
    ARABIC_FONT_SMALL = pygame.font.Font(None, 20)


class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.sound_enabled = True
        self.volume = 0.7

        # Generate sound effects using pygame
        self.create_sounds()

    def create_sounds(self):
        """Create simple sound effects using pygame"""
        try:
            import numpy as np  # تأكد من توفر numpy
            sample_rate = 22050
            duration_click = 0.1
            duration_success = 0.5
            duration_failure = 0.3

            self.sounds = {}
            self.volume = 0.5  # تأكد من تعريفه مسبقًا

            # Click sound
            t_click = np.linspace(0, duration_click, int(sample_rate * duration_click), False)
            wave_click = np.sin(2 * np.pi * 800 * t_click)
            click_sound = (wave_click * 32767).astype(np.int16)
            self.sounds['click'] = pygame.mixer.Sound(buffer=click_sound.tobytes())

            # Success sound - rising tone
            t_success = np.linspace(0, duration_success, int(sample_rate * duration_success), False)
            freqs_up = 440 + (200 * t_success)  # تصاعدي
            wave_success = np.sin(2 * np.pi * freqs_up * t_success)
            success_sound = (wave_success * 32767).astype(np.int16)
            self.sounds['success'] = pygame.mixer.Sound(buffer=success_sound.tobytes())

            # Failure sound - falling tone
            t_failure = np.linspace(0, duration_failure, int(sample_rate * duration_failure), False)
            freqs_down = 440 - (200 * t_failure)  # تنازلي
            wave_failure = np.sin(2 * np.pi * freqs_down * t_failure)
            failure_sound = (wave_failure * 32767).astype(np.int16)
            self.sounds['failure'] = pygame.mixer.Sound(buffer=failure_sound.tobytes())

            for sound in self.sounds.values():
                sound.set_volume(self.volume)

            self.sound_enabled = True

        except Exception as e:
            print(f"Could not create sounds: {e}")
            self.sound_enabled = False

    def create_click_sound(self):
        """Create a click sound effect"""
        duration = 0.1
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = []

        for i in range(frames):
            # Create a short click sound
            wave = 4096 * math.sin(2 * math.pi * 800 * i / sample_rate) * math.exp(-i * 10 / frames)
            arr.append([int(wave), int(wave)])

        sound = pygame.sndarray.make_sound(arr)
        sound.set_volume(self.volume)
        return sound

    def create_success_sound(self):
        """Create a success sound effect"""
        duration = 0.5
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = []

        for i in range(frames):
            # Create ascending notes
            freq = 440 + (i / frames) * 220
            wave = 4096 * math.sin(2 * math.pi * freq * i / sample_rate) * math.exp(-i * 3 / frames)
            arr.append([int(wave), int(wave)])

        sound = pygame.sndarray.make_sound(arr)
        sound.set_volume(self.volume)
        return sound

    def create_failure_sound(self):
        """Create a failure sound effect"""
        duration = 0.3
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = []

        for i in range(frames):
            # Create descending notes
            freq = 440 - (i / frames) * 200
            wave = 4096 * math.sin(2 * math.pi * freq * i / sample_rate) * math.exp(-i * 5 / frames)
            arr.append([int(wave), int(wave)])

        sound = pygame.sndarray.make_sound(arr)
        sound.set_volume(self.volume)
        return sound

    def create_hover_sound(self):
        """Create a hover sound effect"""
        duration = 0.1
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = []

        for i in range(frames):
            # Create a soft hover sound
            wave = 2048 * math.sin(2 * math.pi * 600 * i / sample_rate) * math.exp(-i * 15 / frames)
            arr.append([int(wave), int(wave)])

        sound = pygame.sndarray.make_sound(arr)
        sound.set_volume(self.volume * 0.3)
        return sound

    def create_start_sound(self):
        """Create a game start sound effect"""
        duration = 0.4
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = []

        for i in range(frames):
            # Create a pleasant start sound
            freq = 523 + math.sin(i * 0.01) * 50
            wave = 4096 * math.sin(2 * math.pi * freq * i / sample_rate) * math.exp(-i * 2 / frames)
            arr.append([int(wave), int(wave)])

        sound = pygame.sndarray.make_sound(arr)
        sound.set_volume(self.volume)
        return sound

    def play_sound(self, sound_name):
        """Play a sound effect"""
        if self.sound_enabled and sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except Exception as e:
                print(f"Could not play sound {sound_name}: {e}")

    def toggle_sound(self):
        """Toggle sound on/off"""
        self.sound_enabled = not self.sound_enabled
        return self.sound_enabled


# Arabic text reshaping function
def reshape_arabic_text(text):
    """Properly reshape Arabic text for display"""
    if ARABIC_SUPPORT:
        try:
            # Use proper Arabic reshaping libraries
            reshaped = reshape(text)
            display_text = get_display(reshaped)
            return display_text
        except:
            pass

    # Fallback method with better character mapping
    arabic_map = {
        # Isolated forms to contextual forms mapping
        'ا': 'ﺍ', 'ب': 'ﺏ', 'ت': 'ﺕ', 'ث': 'ﺙ', 'ج': 'ﺝ', 'ح': 'ﺡ', 'خ': 'ﺥ', 'د': 'ﺩ',
        'ذ': 'ﺫ', 'ر': 'ﺭ', 'ز': 'ﺯ', 'س': 'ﺱ', 'ش': 'ﺵ', 'ص': 'ﺹ', 'ض': 'ﺽ', 'ط': 'ﻁ',
        'ظ': 'ﻅ', 'ع': 'ﻉ', 'غ': 'ﻍ', 'ف': 'ﻑ', 'ق': 'ﻕ', 'ك': 'ﻙ', 'ل': 'ﻝ', 'م': 'ﻡ',
        'ن': 'ﻥ', 'ه': 'ﻩ', 'و': 'ﻭ', 'ي': 'ﻱ', 'ى': 'ﻯ', 'ء': 'ﺀ', 'ة': 'ﺓ', 'ئ': 'ﺉ',
        'ؤ': 'ﺅ', 'إ': 'ﺇ', 'أ': 'ﺃ', 'آ': 'ﺁ', 'لا': 'ﻻ'
    }

    # Simple contextual shaping
    result = ""
    for i, char in enumerate(text):
        if char in arabic_map:
            result += arabic_map[char]
        else:
            result += char

    # Reverse for RTL display
    return result[::-1]


def create_arabic_surface(text, font, color):
    """Create a surface with properly shaped Arabic text"""
    try:
        shaped_text = reshape_arabic_text(text)
        return font.render(shaped_text, True, color)
    except:
        # Ultimate fallback
        return font.render(text, True, color)


class Hand:
    def __init__(self, x, y, side, player_name):
        self.x = x
        self.y = y
        self.side = side  # 'left' or 'right'
        self.player_name = player_name
        self.has_ring = False
        self.selected = False
        self.hover = False
        self.was_hovering = False
        self.pulse_timer = 0
        self.glow_intensity = 0
        self.hand_angle = 0
        self.hand_sway_speed = random.uniform(0.02, 0.06)

    def update(self, sound_manager):
        self.pulse_timer += 1
        self.hand_angle += self.hand_sway_speed

        # Play hover sound when first hovering
        if self.hover and not self.was_hovering:
            sound_manager.play_sound('hover')

        self.was_hovering = self.hover

        # Glowing effect for hands
        if self.hover:
            self.glow_intensity = min(self.glow_intensity + 5, 100)
        else:
            self.glow_intensity = max(self.glow_intensity - 5, 0)

    def draw(self, screen):
        # Calculate hand position with slight sway
        sway_x = int(3 * math.sin(self.hand_angle))
        sway_y = int(2 * math.cos(self.hand_angle * 0.8))
        hand_x = self.x + sway_x
        hand_y = self.y + sway_y

        # Draw glow effect if hovering
        if self.glow_intensity > 0:
            glow_color = (255, 255, 255, self.glow_intensity)
            for i in range(3):
                radius = 20 + i * 5
                alpha = max(0, self.glow_intensity - i * 30)
                glow_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, (*YELLOW[:3], alpha), (radius, radius), radius)
                screen.blit(glow_surface, (hand_x - radius, hand_y - radius))

        # Draw hand shadow
        pygame.draw.circle(screen, (0, 0, 0, 50), (hand_x + 2, hand_y + 2), 18)

        # Draw closed fist
        pygame.draw.circle(screen, PINK, (hand_x, hand_y), 18)
        pygame.draw.circle(screen, BLACK, (hand_x, hand_y), 18, 2)

        # Draw fingers as small circles
        finger_positions = [
            (hand_x - 8, hand_y - 12),
            (hand_x, hand_y - 15),
            (hand_x + 8, hand_y - 12),
            (hand_x + 12, hand_y - 5)
        ]

        for pos in finger_positions:
            pygame.draw.circle(screen, PINK, pos, 5)
            pygame.draw.circle(screen, BLACK, pos, 5, 1)

        # Draw thumb
        pygame.draw.circle(screen, PINK, (hand_x - 15, hand_y), 6)
        pygame.draw.circle(screen, BLACK, (hand_x - 15, hand_y), 6, 1)

        # Draw selection indicator
        if self.selected:
            # Pulsing selection ring
            pulse = int(5 * math.sin(self.pulse_timer * 0.1))
            pygame.draw.circle(screen, GOLD, (hand_x, hand_y), 25 + pulse, 3)
            pygame.draw.circle(screen, YELLOW, (hand_x, hand_y), 22 + pulse, 2)

        # Draw side label
        side_text = "يمين" if self.side == "right" else "يسار"
        label_surface = create_arabic_surface(side_text, ARABIC_FONT_SMALL, BLACK)
        label_rect = label_surface.get_rect(center=(hand_x, hand_y + 35))
        screen.blit(label_surface, label_rect)

    def is_clicked(self, pos):
        distance = math.sqrt((pos[0] - self.x) ** 2 + (pos[1] - self.y) ** 2)
        return distance <= 25

    def is_hovered(self, pos):
        distance = math.sqrt((pos[0] - self.x) ** 2 + (pos[1] - self.y) ** 2)
        return distance <= 25


class Player:
    def __init__(self, x, y, name_key, color, is_female=False):
        self.x = x
        self.y = y
        self.name_key = name_key
        self.name = name_key
        self.color = color
        self.is_female = is_female
        self.eye_angle = 0
        self.eye_speed = random.uniform(0.02, 0.05)
        self.blink_timer = 0
        self.is_blinking = False
        self.hair_wave_timer = 0
        self.hair_wave_speed = random.uniform(0.03, 0.07)

        # Create two hands for each player
        self.left_hand = Hand(x - 80, y + 20, "left", name_key)
        self.right_hand = Hand(x + 80, y + 20, "right", name_key)
        self.hands = [self.left_hand, self.right_hand]

    def update(self, sound_manager):
        # Update eye movement
        self.eye_angle += self.eye_speed

        # Update hair wave animation
        self.hair_wave_timer += self.hair_wave_speed

        # Random blinking
        self.blink_timer += 1
        if self.blink_timer > random.randint(120, 300):
            self.is_blinking = True
            self.blink_timer = 0

        if self.is_blinking:
            if self.blink_timer > 10:
                self.is_blinking = False
                self.blink_timer = 0

        # Update hands
        for hand in self.hands:
            hand.update(sound_manager)

    def draw_long_hair(self, screen):
        """Draw long hair for female characters"""
        if not self.is_female:
            return

        # Hair color
        hair_color = DARK_BROWN

        # Draw hair strands with wave animation
        for i in range(12):
            # Left side hair
            wave_offset = int(5 * math.sin(self.hair_wave_timer + i * 0.3))
            start_x = self.x - 35 + i * 3
            start_y = self.y - 100
            end_x = self.x - 60 + i * 2 + wave_offset
            end_y = self.y - 20 + i * 8

            # Draw hair strand
            pygame.draw.line(screen, hair_color, (start_x, start_y), (end_x, end_y), 3)

            # Right side hair
            start_x = self.x + 35 - i * 3
            end_x = self.x + 60 - i * 2 - wave_offset

            pygame.draw.line(screen, hair_color, (start_x, start_y), (end_x, end_y), 3)

        # Draw hair behind head
        for i in range(8):
            angle = (i / 8) * math.pi + math.pi
            wave = int(3 * math.sin(self.hair_wave_timer + i * 0.4))
            hair_x = self.x + int(45 * math.cos(angle)) + wave
            hair_y = self.y - 60 + int(25 * math.sin(angle)) + abs(wave)
            pygame.draw.circle(screen, hair_color, (hair_x, hair_y), 8)

    def draw(self, screen):
        # Draw shadow
        pygame.draw.ellipse(screen, GRAY, (self.x - 48, self.y + 32, 96, 30))

        # Draw long hair behind head for females
        if self.is_female:
            self.draw_long_hair(screen)

        # Draw body
        pygame.draw.ellipse(screen, self.color, (self.x - 50, self.y - 30, 100, 60))
        pygame.draw.ellipse(screen, BLACK, (self.x - 50, self.y - 30, 100, 60), 2)

        # Draw arms extending to hands
        pygame.draw.line(screen, PINK, (self.x - 50, self.y - 10), (self.left_hand.x, self.left_hand.y), 8)
        pygame.draw.line(screen, PINK, (self.x + 50, self.y - 10), (self.right_hand.x, self.right_hand.y), 8)

        # Draw head
        pygame.draw.circle(screen, PINK, (self.x, self.y - 60), 40)
        pygame.draw.circle(screen, BLACK, (self.x, self.y - 60), 40, 2)

        # Draw traditional headwear for males only
        if not self.is_female:
            pygame.draw.arc(screen, BROWN, (self.x - 45, self.y - 105, 90, 50), 0, math.pi, 3)

        # Draw eyes
        if not self.is_blinking:
            # Left eye
            pygame.draw.circle(screen, WHITE, (self.x - 15, self.y - 70), 8)
            pygame.draw.circle(screen, BLACK, (self.x - 15, self.y - 70), 8, 1)
            eye_x = self.x - 15 + int(3 * math.cos(self.eye_angle))
            eye_y = self.y - 70 + int(3 * math.sin(self.eye_angle))
            pygame.draw.circle(screen, BLACK, (eye_x, eye_y), 3)

            # Right eye
            pygame.draw.circle(screen, WHITE, (self.x + 15, self.y - 70), 8)
            pygame.draw.circle(screen, BLACK, (self.x + 15, self.y - 70), 8, 1)
            eye_x = self.x + 15 + int(3 * math.cos(self.eye_angle + 0.1))
            eye_y = self.y - 70 + int(3 * math.sin(self.eye_angle + 0.1))
            pygame.draw.circle(screen, BLACK, (eye_x, eye_y), 3)
        else:
            # Blinking eyes (lines)
            pygame.draw.line(screen, BLACK, (self.x - 23, self.y - 70), (self.x - 7, self.y - 70), 2)
            pygame.draw.line(screen, BLACK, (self.x + 7, self.y - 70), (self.x + 23, self.y - 70), 2)

        # Draw smile
        pygame.draw.arc(screen, BLACK, (self.x - 15, self.y - 55, 30, 20), 0, math.pi, 2)

        # Draw hands
        for hand in self.hands:
            hand.draw(screen)

        # Draw name (Arabic)
        name_surface = create_arabic_surface(self.name, ARABIC_FONT, BLACK)
        name_rect = name_surface.get_rect(center=(self.x, self.y + 80))
        screen.blit(name_surface, name_rect)


# Arabic names and texts
ARABIC_NAMES = {
    'احمد': 'أحمد',
    'فرح': 'فرح',
    'محمد': 'محمد',
    'زينب': 'زينب'
}

ARABIC_TEXTS = {
    'title': 'لعبة المحيبس',
    'start': 'اضغط مسطرة للبدء',
    'hidden': 'الخاتم مخفي! اضغط على اليد',
    'correct': 'مبروك! الخاتم كان في يد',
    'wrong': 'خطأ! الخاتم كان في يد',
    'rules': 'قواعد اللعبة:',
    'rule1': '1. اضغط مسطرة لبدء جولة جديدة',
    'rule2': '2. الخاتم مخفي في يد واحدة',
    'rule3': '3. اضغط على اليد التي تظن أن الخاتم فيها',
    'rule4': '4. اضغط R لإعادة تشغيل اللعبة',
    'rule5': '5. اضغط M لكتم/إلغاء كتم الصوت',
    'left': 'يسار',
    'right': 'يمين',
    'player': 'لاعب',
    'hand_of': 'يد',
    'space_to_start': 'اضغط مسطرة للبدء',
    'click_hand': 'اضغط على اليد',
    'sound_on': 'الصوت مفعل',
    'sound_off': 'الصوت معطل'
}


class MahaybesGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("لعبة المحيبس - Mahaybes Game")
        self.clock = pygame.time.Clock()

        # Initialize sound manager
        self.sound_manager = SoundManager()

        # Background gradient colors
        self.bg_color1 = (250, 248, 240)
        self.bg_color2 = (245, 245, 220)

        # Create players with Arabic names - females have long hair
        self.players = [
            Player(300, 300, 'أحمد', BLUE, is_female=False),
            Player(900, 300, 'فرح', GREEN, is_female=True),
            Player(300, 600, 'محمد', RED, is_female=False),
            Player(900, 600, 'زينب', ORANGE, is_female=True)
        ]

        # Collect all hands
        self.all_hands = []
        for player in self.players:
            self.all_hands.extend(player.hands)

        self.game_state = "waiting"
        self.ring_hand = None
        self.selected_hand = None
        self.current_message = 'start'
        self.winner_info = ""
        self.animation_timer = 0
        self.show_ring_animation = False
        self.mouse_pos = (0, 0)
        self.sound_status_timer = 0

    def draw_gradient_background(self):
        """Draw a gradient background"""
        for y in range(HEIGHT):
            ratio = y / HEIGHT
            r = int(self.bg_color1[0] * (1 - ratio) + self.bg_color2[0] * ratio)
            g = int(self.bg_color1[1] * (1 - ratio) + self.bg_color2[1] * ratio)
            b = int(self.bg_color1[2] * (1 - ratio) + self.bg_color2[2] * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (WIDTH, y))

    def draw_traditional_border(self):
        """Draw traditional Islamic geometric border"""
        # Draw decorative border
        pygame.draw.rect(self.screen, BROWN, (10, 10, WIDTH - 20, HEIGHT - 20), 5)
        pygame.draw.rect(self.screen, YELLOW, (15, 15, WIDTH - 30, HEIGHT - 30), 2)

        # Draw corner decorations
        corners = [(30, 30), (WIDTH - 30, 30), (30, HEIGHT - 30), (WIDTH - 30, HEIGHT - 30)]
        for corner in corners:
            pygame.draw.circle(self.screen, BROWN, corner, 15)
            pygame.draw.circle(self.screen, YELLOW, corner, 10)

    def start_round(self):
        # Reset all hands
        for hand in self.all_hands:
            hand.has_ring = False
            hand.selected = False

        # Randomly select which hand has the ring
        self.ring_hand = random.choice(self.all_hands)
        self.ring_hand.has_ring = True

        self.game_state = "hiding"
        self.current_message = 'hidden'
        self.animation_timer = 0
        self.show_ring_animation = False

        # Play start sound
        self.sound_manager.play_sound('start')

    def handle_click(self, pos):
        if self.game_state == "hiding":
            # Check if clicked on any hand
            for hand in self.all_hands:
                if hand.is_clicked(pos):
                    self.selected_hand = hand
                    hand.selected = True
                    self.game_state = "result"
                    self.show_ring_animation = True
                    self.animation_timer = 0

                    # Play click sound
                    self.sound_manager.play_sound('click')

                    # Create winner info text
                    side_text = "اليمين" if self.ring_hand.side == "right" else "اليسار"
                    self.winner_info = f"{side_text} {self.ring_hand.player_name}"

                    if hand == self.ring_hand:
                        self.current_message = 'correct'
                        self.sound_manager.play_sound('success')
                    else:
                        self.current_message = 'wrong'
                        self.sound_manager.play_sound('failure')
                    break

    def handle_mouse_motion(self, pos):
        self.mouse_pos = pos
        # Update hover state for all hands
        for hand in self.all_hands:
            hand.hover = hand.is_hovered(pos) and self.game_state == "hiding"

    def draw_arabic_text(self, text, pos, font, color=BLACK):
        """Draw Arabic text on screen"""
        text_surface = create_arabic_surface(text, font, color)
        text_rect = text_surface.get_rect(center=pos)
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def draw_instructions(self):
        # Draw game title with decorative elements
        title_rect = self.draw_arabic_text(ARABIC_TEXTS['title'], (WIDTH // 2, 60), ARABIC_FONT_LARGE, BROWN)

        # Draw decorative lines around title
        pygame.draw.line(self.screen, BROWN, (title_rect.left - 30, title_rect.centery),
                         (title_rect.left - 10, title_rect.centery), 3)
        pygame.draw.line(self.screen, BROWN, (title_rect.right + 10, title_rect.centery),
                         (title_rect.right + 30, title_rect.centery), 3)

        # Draw instructions in bottom area
        instructions = [
            (ARABIC_TEXTS['rules'], 720),
            (ARABIC_TEXTS['rule1'], 740),
            (ARABIC_TEXTS['rule2'], 760),
            (ARABIC_TEXTS['rule3'], 780),
            (ARABIC_TEXTS['rule4'], 800),
            (ARABIC_TEXTS['rule5'], 820)
        ]

        for text, y in instructions:
            if y < HEIGHT - 20:  # Make sure it fits on screen
                self.draw_arabic_text(text, (WIDTH // 2, y), ARABIC_FONT_SMALL)

    def draw_message(self):
        # Draw current message with animation
        message_y = 120

        if self.current_message == 'correct':
            self.draw_arabic_text(ARABIC_TEXTS['correct'], (WIDTH // 2 - 100, message_y), ARABIC_FONT, GREEN)
            self.draw_arabic_text(self.winner_info, (WIDTH // 2 + 80, message_y), ARABIC_FONT, GREEN)

        elif self.current_message == 'wrong':
            self.draw_arabic_text(ARABIC_TEXTS['wrong'], (WIDTH // 2 - 100, message_y), ARABIC_FONT, RED)
            self.draw_arabic_text(self.winner_info, (WIDTH // 2 + 80, message_y), ARABIC_FONT, RED)

        elif self.current_message == 'start':
            pulse = int(5 * math.sin(pygame.time.get_ticks() * 0.005))
            color_intensity = 100 + pulse * 10
            pulse_color = (0, 0, min(255, color_intensity))
            self.draw_arabic_text(ARABIC_TEXTS['start'], (WIDTH // 2, message_y), ARABIC_FONT, pulse_color)

        else:
            self.draw_arabic_text(ARABIC_TEXTS[self.current_message], (WIDTH // 2, message_y), ARABIC_FONT)

            # Draw ring indicator
        if self.game_state == "result" and self.ring_hand and self.show_ring_animation:
            self.animation_timer += 1
            ring_y = self.ring_hand.y - 40 + int(8 * math.sin(self.animation_timer * 0.08))
            ring_radius = 20 + int(3 * math.sin(self.animation_timer * 0.1))
            pygame.draw.circle(self.screen, GOLD, (self.ring_hand.x, ring_y), ring_radius, 4)
            pygame.draw.circle(self.screen, YELLOW, (self.ring_hand.x, ring_y), ring_radius - 5, 3)
            pygame.draw.circle(self.screen, RED, (self.ring_hand.x, ring_y), 8)
            pygame.draw.circle(self.screen, WHITE, (self.ring_hand.x - 3, ring_y - 3), 3)

    def run(self):
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            if self.game_state in ["waiting", "result"]:
                                self.start_round()
                        elif event.key == pygame.K_r:
                            self.__init__()
                        elif event.key == pygame.K_m:
                            status = self.sound_manager.toggle_sound()
                            self.sound_status_timer = pygame.time.get_ticks()
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.handle_click(event.pos)
                    elif event.type == pygame.MOUSEMOTION:
                        self.handle_mouse_motion(event.pos)

                for player in self.players:
                    player.update(self.sound_manager)

                self.draw_gradient_background()
                self.draw_traditional_border()

                for player in self.players:
                    player.draw(self.screen)

                self.draw_message()
                self.draw_instructions()

                # Show sound status briefly
                if pygame.time.get_ticks() - self.sound_status_timer < 2000:
                    text = ARABIC_TEXTS['sound_on'] if self.sound_manager.sound_enabled else ARABIC_TEXTS['sound_off']
                    self.draw_arabic_text(text, (WIDTH // 2, 160), ARABIC_FONT_SMALL, PURPLE)

                pygame.display.flip()
                self.clock.tick(FPS)

            pygame.quit()
            sys.exit()
if __name__ == "__main__":
    print("بدء تشغيل لعبة المحيبس - إختر اليد!")
    if not ARABIC_SUPPORT:
        print("⚠️  للحصول على أفضل عرض للنص العربي، ثبت:")
        print("pip install arabic-reshaper python-bidi")
    game = MahaybesGame()
    game.run()
