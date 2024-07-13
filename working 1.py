
import pygame
import threading

pygame.init()

pygame.display.set_caption("THE ARDUINO")
screen = pygame.display.set_mode((900, 700), pygame.RESIZABLE)
font = pygame.font.Font(None, 24)  # Font for rendering text

# Vars
ardinos = []
items = []
mouse_stats = None

def const(x, min, max):
    if x > max:
        return max
    elif x < min:
        return min
    else:
        return x

# Class definition
class LED:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id
        self.bindPin = None  # Initialize bindPin to None initially
        self.state = False  # LED state initially off

    def draw(self):
        if self.bindPin is not None:
            self.state = self.bindPin[0].pins[self.bindPin[1]]# Update LED state based on bindPin
            x = self.state
            if type(self.state) == bool and self.state:
                x = 255
            elif type(self.state) == bool and not self.state:
                x = 0
            
            pygame.draw.line(screen, (x, 44, 44), (self.x, self.y), (self.bindPin[0].x, self.bindPin[0].x))
        led_color = (255, 0, 0) if self.state else (100, 0, 0)
        led_size = 10
        pygame.draw.rect(screen, led_color, (self.x, self.y, led_size, led_size))

    def BindToPin(self, item, pinname):
        self.bindPin = [item, pinname]


class Arduino:
    def __init__(self, x, y, code, startupcode, id) -> None:
        self.x = x
        self.y = y
        self.width = 100  # Base width of the Arduino object
        self.height = 200  # Base height of the Arduino object
        self.codeloop = code
        self.startupcode = startupcode
        self.pins = {
            "Pin1": False, "Pin2": False, "Pin3": False, "Pin4": False, "Pin5": False,
            "Pin6": False, "Pin7": False, "Pin8": False, "Pin9": False, "PinA0": 0,
            "PinA1": 0, "PinA2": 0, "PinA3": 0, "PinA4": 0
        }
        self.id = id
        self.inbuiltled_State = False
        self.startup = False
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True  # Ensures the thread exits when the main program does
        self.thread.start()
        self.selected = False  # Flag to indicate if the Arduino is selected

        # Text rendering for UNO NANO
        self.text_surfaces = []
        text = "UNO NANO"
        for i, char in enumerate(text):
            text_render = font.render(char, True, (0, 0, 0))  # Render each character in black
            self.text_surfaces.append(text_render)

    def draw(self):
        # Draw the main body of the Arduino
        main_color = (150, 150, 255) if not self.selected else (0, 255, 0)  # Green if selected, otherwise blue
        pygame.draw.rect(screen, main_color, (self.x, self.y, self.width, self.height))

        # Determine LED color and position (top right corner)
        led_color = (255, 0, 0) if self.inbuiltled_State else (100, 0, 0)  # Red if on, dark red if off
        led_size = min(self.width, self.height) // 8  # Adjusted size of the LED square
        led_x = self.x + self.width - led_size - 5
        led_y = self.y + 5
        pygame.draw.rect(screen, led_color, (led_x, led_y, led_size, led_size))

        # Draw digital pins (to the left of the Arduino body)
        pin_size = 10
        pin_spacing = 15
        pin_x = self.x - pin_spacing - pin_size + 35
        for i, (pin, state) in enumerate(self.pins.items()):
            if i < 9:  # Limit to the first 9 digital pins
                pin_y = self.y + self.height // 2 - pin_spacing * 6 + i * pin_spacing
                pin_color = (200, 200, 200) if state else (0, 0, 0)  # Gray if True, black if False
                pygame.draw.rect(screen, pin_color, (pin_x, pin_y, pin_size, pin_size))

        # Draw analog pins as an array of squares (at the bottom of the Arduino body)
        analog_pin_size = 10
        analog_pin_spacing = 15
        analog_pins = ["PinA0", "PinA1", "PinA2", "PinA3", "PinA4"]
        for i, pin in enumerate(analog_pins):
            analog_pin_x = self.x + self.width // 2 - analog_pin_spacing * 2.5 + i * analog_pin_spacing
            analog_pin_y = self.y + self.height + analog_pin_spacing - 35  # Add an offset to avoid floating pins
            analog_pin_gray = int(self.pins[pin] / 255 * 255)  # Scale value to gray color
            analog_pin_color = (analog_pin_gray, analog_pin_gray, analog_pin_gray)
            pygame.draw.rect(screen, analog_pin_color, (analog_pin_x, analog_pin_y, analog_pin_size, analog_pin_size))

        # Draw text "UNO NANO" vertically
        text_x = self.x + self.width // 2 - 10  # Adjust horizontally to center
        text_y = self.y + 10  # Top margin
        text_height = font.get_linesize()
        for i, surface in enumerate(self.text_surfaces):
            text_render_pos = (text_x, text_y + i * text_height)
            screen.blit(surface, text_render_pos)

    def run(self):
        local_vars = {"self": self}
        while True:
            if not self.startup:
                exec(self.startupcode, {}, local_vars)
                self.startup = True
            else:
                exec(self.codeloop, {}, local_vars)

    def check_mouse_over(self, mouse_pos):
        # Check if the mouse is over the Arduino object
        return (self.x <= mouse_pos[0] <= self.x + self.width and
                self.y <= mouse_pos[1] <= self.y + self.height)

    def get_stats(self):
        # Generate stats text to render
        stats = []
        stats.append(f"Arduino ID: {self.id}")
        stats.append(f"Position: ({self.x}, {self.y})")
        stats.append("Digital Pins:")
        for i, (pin, state) in enumerate(self.pins.items()):
            if i < 9:  # Display only the first 9 digital pins
                stats.append(f"{pin}: {state}")
        stats.append("Analog Pins:")
        for pin in ["PinA0", "PinA1", "PinA2", "PinA3", "PinA4"]:
            # Check analog pin value range
            analog_value = self.pins[pin]
            if analog_value < 0:
                analog_value = 0
            elif analog_value > 255:
                analog_value = 255
            stats.append(f"{pin}: {analog_value}")
        stats.append(f"Inbuilt LED: {self.inbuiltled_State}")
        return stats

    def display_stats(self, mouse_pos):
        # Display stats as text near the mouse position if the Arduino is selected
        if self.selected:
            stats = self.get_stats()
            text_height = font.get_linesize()
            text_pos_x = mouse_pos[0] + 10
            text_pos_y = mouse_pos[1] - len(stats) * text_height // 2

            for i, stat in enumerate(stats):
                text_render = font.render(stat, True, (0, 0, 0))
                screen.blit(text_render, (text_pos_x, text_pos_y + i * text_height))

# Adding Arduino instances
ardinos.append(Arduino(350, 150, '''
import time
wait = 0.1
while True:
    self.inbuiltled_State = True
    for i in range(len(self.pins)):
        i += 1
        if i < 10:
            self.pins[f"Pin{i}"] = True
            time.sleep(wait)
    self.inbuiltled_State = False
    for i in range(len(self.pins)):
        if i < 10:
            self.pins[f"Pin{i}"] = False
            time.sleep(wait)

''', "", len(ardinos)))

for x in range(9):
    led = LED(200, 150 + 10 * x, len(items))  # Create LED instance
    led.BindToPin(ardinos[0], f'Pin{x + 1}')  # Bind LED to Arduino pin
    items.append(led)  # Add LED to items list

# Main loop
running = True
clock = pygame.time.Clock()
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if a mouse click happened
            mouse_pos = pygame.mouse.get_pos()
            for arduino in ardinos:
                if arduino.check_mouse_over(mouse_pos):
                    arduino.selected = True
                    mouse_stats = arduino
                else:
                    arduino.selected = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        items.append(LED(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], len(items)))
    if keys[pygame.K_e]:
        pass
    for arduino in ardinos:
        arduino.draw()
    for item in items:
        item.draw()

    # Display mouse stats if available
    if mouse_stats:
        mouse_stats.display_stats(pygame.mouse.get_pos())

    pygame.display.flip()
    clock.tick(30)

pygame.quit()