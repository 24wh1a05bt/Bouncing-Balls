import pygame
import random
import os
import math

# Initialize Pygame and Mixer for sound
pygame.init()

pygame.mixer.init()

correct_sound = pygame.mixer.Sound(r"C:\Users\charvi parmar\Downloads\correct.mp3")
wrong_sound = pygame.mixer.Sound(r"C:\Users\charvi parmar\Downloads\wrong.mp3")
game_over_sound = pygame.mixer.Sound(r"C:\Users\charvi parmar\Downloads\gameover.wav")
menu_select_sound = pygame.mixer.Sound(r"C:\Users\charvi parmar\Downloads\menuselect.mp3")

# Screen dimensions
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BOUNCING BALL")
main_menu_background = pygame.image.load(r"C:\Users\charvi parmar\Downloads\Main menu logo.jpg")
main_menu_background = pygame.transform.scale(main_menu_background, (WIDTH, HEIGHT))
game_background = pygame.image.load(r"C:\Users\charvi parmar\Downloads\Main game background.png").convert()
game_background = pygame.transform.scale(game_background, (WIDTH, HEIGHT))

# Colors
COLORS = {
    "red": (255, 0, 0),
    "blue": (0, 0, 255),
    "green": (0, 255, 0),
    "yellow": (255, 255, 0)
}
color_names = list(COLORS.keys())

# Fonts
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)

# Ball setup
ball_radius = 20

def reset_ball():
    color_name = random.choice(color_names)
    return {"x": random.randint(ball_radius, WIDTH - ball_radius), "y": -ball_radius, "color": COLORS[color_name], "name": color_name}

# Bins setup
def create_bins():
    bins = []
    bin_width = WIDTH // len(COLORS)
    for i, color in enumerate(color_names):
        bins.append({
            "x": i * bin_width + bin_width // 2,
            "y": HEIGHT - 100,
            "color": COLORS[color],
            "name": color
        })
    return bins

bins = create_bins()

# Game state variables
clock = pygame.time.Clock()
running = True
in_main_menu = True
game_over = False
paused = False

score = 0
wrong_drops = 0
max_wrong = 3
ball_speed_y = 5
speed_milestone = 0
balls = [reset_ball()]
current_ball_index = 0

# Load high score
if os.path.exists("high_score.txt"):
    with open("high_score.txt", "r") as f:
        try:
            high_score = int(f.read())
        except:
            high_score = 0
else:
    high_score = 0

def save_high_score():
    with open("high_score.txt", "w") as f:
        f.write(str(high_score))

def draw_bins():
    bin_width = 100
    bin_height = 75
    for bin in bins:
        rect = pygame.Rect(bin["x"] - bin_width // 2, bin["y"] - bin_height // 2, bin_width, bin_height)
        pygame.draw.rect(screen, bin["color"], rect, border_radius=15)
        gloss_rect = pygame.Rect(rect.x, rect.y, bin_width, bin_height // 2)
        pygame.draw.rect(screen, (255, 255, 255, 80), gloss_rect, border_radius=15)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2, border_radius=15)

def show_main_menu():
    screen.blit(main_menu_background, (0, 0))  # Draw the background image
    start_text = font.render("Press SPACE to Start", True, (0, 128, 0))
    quit_text = font.render("Press ESC to Quit", True, (128, 0, 0))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 500))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, 550))

    pygame.display.flip()

def show_game_over():
    screen.fill((0, 0, 0))
    over_text = big_font.render("GAME OVER", True, (255, 0, 0))
    final_score = font.render(f"Score: {score}", True, (255, 255, 255))
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
    restart_text = font.render("Press SPACE to Restart", True, (0, 255, 0))
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
    screen.blit(game_background, (0, 0))
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(50)  # Adjust transparency
    overlay.fill((0, 0, 0))  # Black overlay
    screen.blit(overlay, (0, 0))

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_high_score()
            running = False

        elif event.type == pygame.KEYDOWN:
            if in_main_menu and event.key == pygame.K_SPACE:
                menu_select_sound.play()
                in_main_menu = False
                reset_game()
            elif event.key == pygame.K_ESCAPE:
                confirm_quit = True
                while confirm_quit:
                    screen.fill((0, 0, 0))
                    quit_msg = font.render("Are you sure you want to quit? (Y/N)", True, (255, 255, 255))
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
                                for i in range(3, 0, -1):
                                    screen.blit(game_background, (0, 0))
                                    for ball in balls:
                                        pygame.draw.circle(screen, ball["color"], (ball["x"], ball["y"]), ball_radius)
                                    draw_bins()
                                    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
                                    screen.blit(score_text, (10, 10))
                                    high_score_text = font.render(f"High Score: {high_score}", True, (0, 0, 0))
                                    screen.blit(high_score_text, (10, 40))
                                    wrong_drops_text = font.render(f"Missed: {wrong_drops}/{max_wrong}", True, (255, 0, 0))
                                    screen.blit(wrong_drops_text, (10, 70))
                                    countdown_text = big_font.render(str(i), True, (0, 0, 255))
                                    screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2))
                                    pygame.display.flip()
                                    pygame.time.delay(1000)
                                    confirm_quit = False
            elif game_over and event.key == pygame.K_SPACE:
                reset_game()
            elif not paused and event.key == pygame.K_p:
                paused = True
            elif paused and event.key == pygame.K_r:
                paused = False
                for i in range(3, 0, -1):
                    screen.blit(game_background, (0, 0))
                    for ball in balls:
                        pygame.draw.circle(screen, ball["color"], (ball["x"], ball["y"]), ball_radius)
                    draw_bins()
                    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
                    screen.blit(score_text, (10, 10))
                    high_score_text = font.render(f"High Score: {high_score}", True, (0, 0, 0))
                    screen.blit(high_score_text, (10, 40))
                    wrong_drops_text = font.render(f"Missed: {wrong_drops}/{max_wrong}", True, (255, 0, 0))
                    screen.blit(wrong_drops_text, (10, 70))
                    countdown_text = big_font.render(str(i), True, (0, 0, 255))
                    screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2))
                    pygame.display.flip()
                    pygame.time.delay(1000)
                    paused = False


    if in_main_menu:
        show_main_menu()
        
    elif game_over:
        show_game_over()

    elif paused:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        pause_text = big_font.render("Paused", True, (255, 255, 255))
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()

    else:
        if keys[pygame.K_LEFT]:
            balls[current_ball_index]["x"] -= 7
        if keys[pygame.K_RIGHT]:
            balls[current_ball_index]["x"] += 7

        new_balls = []
        for ball in balls:
            ball["y"] += ball_speed_y
            shadow = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(shadow, (*ball["color"], 60), (20, 20), 20)
            screen.blit(shadow, (ball["x"] - 20, ball["y"] - 20))
            pygame.draw.circle(screen, (0, 0, 0), (ball["x"], ball["y"]), ball_radius + 2)  # Black border
            pygame.draw.circle(screen, ball["color"], (ball["x"], ball["y"]), ball_radius)  # Inner colored ball


            if ball["y"] + ball_radius >= HEIGHT - 100:
                matched = False
                for bin in bins:
                    if bin["x"] - 50 < ball["x"] < bin["x"] + 50 and bin["name"] == ball["name"]:
                        score += 1
                        matched = True
                        correct_sound.play()
                        break
                if not matched:
                    wrong_drops += 1
                    wrong_sound.play()

                if wrong_drops >= max_wrong:
                    game_over = True
                    game_over_sound.play()
                    if score > high_score:
                        high_score = score
                        save_high_score()
                else:
                    new_balls.append(reset_ball())
            else:
                new_balls.append(ball)

        balls = new_balls

        if score // 10 > speed_milestone:
            ball_speed_y += 1
            speed_milestone = score // 10

        draw_bins()

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 0), (5, 5, score_text.get_width() + 10, 30), border_radius=5)
        screen.blit(score_text, (10, 10))

        high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
        screen.blit(high_score_text, (10, 40))

        wrong_drops_text = font.render(f"Missed: {wrong_drops}/{max_wrong}", True, (255, 100, 100))
        screen.blit(wrong_drops_text, (10, 70))

        pygame.display.update()
        clock.tick(60)

pygame.quit()