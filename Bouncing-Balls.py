import pygame
import random
import os


# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BOUNCING BALL")

# Fonts
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)

# Ball setup
ball_radius = 20

# Game state variables
clock = pygame.time.Clock()
running = True
in_main_menu = True
game_over = False
paused = False

score = 0
high_score = 0
wrong_drops = 0
max_wrong = 3
ball_speed_y = 5
speed_milestone = 0
balls = []
current_ball_index = 0

# Ball colors
COLORS = {
    "red": (255, 0, 0),
    "blue": (0, 0, 255),
    "green": (0, 255, 0),
    "yellow": (255, 255, 0)
}

# Themes
THEMES = {
    "basic": {
        "background": (255, 255, 255),
        "bin_color": (100, 100, 100),
        "ball_colors": COLORS
    },
    "basketball": {
        "background": (255, 153, 51),
        "bin_color": (255, 102, 0),
        "ball_colors": {
            "red": (255, 0, 0),
            "orange": (255, 165, 0),
            "black": (0, 0, 0),
            "white": (255, 255, 255)
        }
    },
    "forest": {
        "background": (34, 139, 34),
        "bin_color": (0, 100, 0),
        "ball_colors": {
            "green": (0, 255, 0),
            "brown": (139, 69, 19),
            "yellow": (255, 255, 0),
            "red": (255, 0, 0)
        }
    }
}

selected_theme = "basic"
color_names = list(THEMES[selected_theme]["ball_colors"].keys())

# Theme buttons
theme_buttons = {}

# Load high score
if os.path.exists("high_score.txt"):
    with open("high_score.txt", "r") as f:
        try:
            high_score = int(f.read())
        except:
            high_score = 0

def save_high_score():
    with open("high_score.txt", "w") as f:
        f.write(str(high_score))

def reset_ball():
    color_name = random.choice(list(THEMES[selected_theme]["ball_colors"].keys()))
    return {
        "x": random.randint(ball_radius, WIDTH - ball_radius),
        "y": -ball_radius,
        "color": THEMES[selected_theme]["ball_colors"][color_name],
        "name": color_name
    }

# Bins
def create_bins():
    theme_colors = THEMES[selected_theme]["ball_colors"]
    bins = []
    bin_width = WIDTH // len(theme_colors)
    for i, color_name in enumerate(theme_colors.keys()):
        bins.append({
            "x": i * bin_width + bin_width // 2,
            "y": HEIGHT - 100,
            "color": theme_colors[color_name],
            "name": color_name
        })
    return bins

bins = create_bins()

def draw_bins():
    bin_width = 100
    bin_height = 60
    for bin in bins:
        rect = pygame.Rect(bin["x"] - bin_width // 2, bin["y"] - bin_height // 2, bin_width, bin_height)
        pygame.draw.rect(screen, bin["color"], rect, border_radius=15)  # Rounded rectangle
        pygame.draw.rect(screen, (0, 0, 0), rect, 2, border_radius=15)  # Border for better visibility
        label = font.render(bin["name"].capitalize(), True, (0, 0, 0))
        screen.blit(label, (bin["x"] - label.get_width() // 2, bin["y"] + bin_height // 2 + 5))

def show_main_menu():
    screen.fill((255, 255, 255))
    title = big_font.render("BOUNCING BALL", True, (0, 0, 0))
    start_text = font.render("Press SPACE to Start", True, (0, 128, 0))
    quit_text = font.render("Press ESC to Quit", True, (128, 0, 0))
    theme_label = font.render("Choose Theme:", True, (0, 0, 0))

    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 200))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, 250))
    screen.blit(theme_label, (WIDTH // 2 - theme_label.get_width() // 2, 320))

    theme_y = 360
    theme_buttons.clear()
    for idx, theme_name in enumerate(THEMES.keys()):
        selected = selected_theme == theme_name
        color = (0, 0, 255) if selected else (0, 0, 0)
        theme_text = font.render(theme_name.capitalize() + (" (Selected)" if selected else ""), True, color)
        rect = theme_text.get_rect(center=(WIDTH // 2, theme_y + idx * 40))
        theme_buttons[theme_name] = rect
        screen.blit(theme_text, rect)

    pygame.display.flip()

def show_game_over():
    screen.fill((255, 255, 255))
    over_text = big_font.render("GAME OVER", True, (255, 0, 0))
    final_score = font.render(f"Score: {score}", True, (0, 0, 0))
    high_score_text = font.render(f"High Score: {high_score}", True, (0, 0, 0))
    restart_text = font.render("Press SPACE to Restart", True, (0, 128, 0))

    screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 60))
    screen.blit(final_score, (WIDTH // 2 - final_score.get_width() // 2, HEIGHT // 2))
    screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 + 40))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 80))

    pygame.display.flip()

def reset_game():
    global score, wrong_drops, ball_speed_y, balls, current_ball_index, game_over, bins, speed_milestone
    score = 0
    wrong_drops = 0
    ball_speed_y = 5
    speed_milestone = 0
    balls = [reset_ball()]
    current_ball_index = 0
    game_over = False
    bins = create_bins()

# Game loop
while running:
    screen.fill(THEMES[selected_theme]["background"])
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_high_score()
            running = False

        elif event.type == pygame.KEYDOWN:
            if in_main_menu and event.key == pygame.K_SPACE:
                in_main_menu = False
                reset_game()
            elif event.key == pygame.K_ESCAPE:
                confirm_quit = True
                while confirm_quit:
                    screen.fill((255, 255, 255))
                    quit_msg = font.render("Are you sure you want to quit? (Y/N)", True, (0, 0, 0))
                    screen.blit(quit_msg, (WIDTH // 2 - quit_msg.get_width() // 2, HEIGHT // 2))
                    pygame.display.flip()
                    for quit_event in pygame.event.get():
                        if quit_event.type == pygame.QUIT:
                            confirm_quit = False
                            running = False
                        elif quit_event.type == pygame.KEYDOWN:
                            if quit_event.key == pygame.K_y:
                                running = False
                                confirm_quit = False
                            elif quit_event.key == pygame.K_n:
                                confirm_quit = False   
            elif game_over and event.key == pygame.K_SPACE:
                reset_game()
            elif not paused and event.key == pygame.K_p:
                paused = True
            elif paused and event.key == pygame.K_r:
                paused = False

        elif event.type == pygame.MOUSEBUTTONDOWN and in_main_menu:
            pos = pygame.mouse.get_pos()
            for theme_name, rect in theme_buttons.items():
                if rect.collidepoint(pos):
                    selected_theme = theme_name
                    color_names = list(THEMES[selected_theme]["ball_colors"].keys())
                    bins = create_bins()

    if in_main_menu:
        show_main_menu()

    elif game_over:
        show_game_over()

    elif paused:
        pause_text = big_font.render("Paused", True, (0, 0, 255))
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()

    else:
        # Move ball left/right
        if keys[pygame.K_LEFT]:
            balls[current_ball_index]["x"] -= 7
        if keys[pygame.K_RIGHT]:
            balls[current_ball_index]["x"] += 7

        new_balls = []
        for ball in balls:
            ball["y"] += ball_speed_y
            pygame.draw.circle(screen, ball["color"], (ball["x"], ball["y"]), ball_radius)

            # Check if ball hits bin area
            if ball["y"] + ball_radius >= HEIGHT - 100:
                matched = False
                for bin in bins:
                    if bin["x"] - 50 < ball["x"] < bin["x"] + 50 and bin["name"] == ball["name"]:
                        score += 1
                        matched = True
                        break
                if not matched:
                    wrong_drops += 1

                if wrong_drops >= max_wrong:
                    game_over = True
                    if score > high_score:
                        high_score = score
                        save_high_score()
                else:
                    new_balls.append(reset_ball())
            else:
                new_balls.append(ball)

        balls = new_balls

        # Increase speed every 10 points
        if score // 10 > speed_milestone:
            ball_speed_y += 1
            speed_milestone = score // 10

        draw_bins()

        # Draw UI
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        high_score_text = font.render(f"High Score: {high_score}", True, (0, 0, 0))
        screen.blit(high_score_text, (10, 40))

        wrong_drops_text = font.render(f"Missed: {wrong_drops}/{max_wrong}", True, (255, 0, 0))
        screen.blit(wrong_drops_text, (10, 70))

        pygame.display.update()
        clock.tick(60)

pygame.quit()