import pygame
import os
import random


pygame.font.init()

# Player/icon
Player_ship = pygame.image.load(os.path.join("PLAYERSHIP.png"))


# setup
WIDTH, HEIGHT = 1000, 700
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders By Shivansh ! ! !")
pygame.display.set_icon(Player_ship)
# win.get_window_size()


# Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("pixel_ship_blue_small.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("pixel_laser_yellow.png"))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("background-black.png")), (WIDTH, HEIGHT))

# Pause and play
PAUSE = pygame.transform.scale(pygame.image.load(os.path.join("Pause.png")), (50,50))
PLAY = pygame.transform.scale(pygame.image.load(os.path.join("Play.png")), (50,50))

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


class Ship:
    COOLDOWN = 30

    def __init__(self, x, y, health=10000):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
            
    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = Player_ship
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs, SCORE):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                            SCORE += 1

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))


class Enemy(Ship):
    COLOR_MAP = {
                "red": (RED_SPACE_SHIP, RED_LASER),
                "green": (GREEN_SPACE_SHIP, GREEN_LASER),
                "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
                }

    def __init__(self, x, y, color, health=175):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main():
    run = True
    FPS = 120
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    enemies = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 5
    laser_vel = 10

    player = Player(300, 630)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    SCORE = 0


    condition = False

    # score_font = pygame.font.SysFont("comicsans", 50)

    def redraw_window(SCORE):
        win.blit(BG, (0,0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))
        wave_label = main_font.render(f"Wave: {level}", 1, (255,255,255))

        win.blit(lives_label, (10, 10))
        win.blit(level_label, (860,10))
        win.blit(wave_label, (425, 15))
        win.blit(PAUSE, (0, HEIGHT - 50))


        for enemy in enemies:
            enemy.draw(win)

        player.draw(win)

        if lost:
            lost_label = lost_font.render("You Lost!!", 1, (255,255,255))
            win.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        pygame.display.update()


    while run:
        clock.tick(FPS)
        redraw_window(SCORE)

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 1
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                if (m_x > 0 and m_x <50) and (m_y > HEIGHT-50 and m_y < HEIGHT):
                    pause()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player.x - player_vel > 0: # left
                player.x -= player_vel
            if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH: # right
                player.x += player_vel
            if keys[pygame.K_UP] and player.y - player_vel > 0: # up
                player.y -= player_vel
            if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() + 15 < HEIGHT: # down
                player.y += player_vel
            if keys[pygame.K_SPACE]:
                player.shoot()
            if keys[pygame.K_p]:
                pause()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies, SCORE)
        # print(SCORE)


def pause():
    pause = True

    keys = pygame.key.get_pressed()
    

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_menu()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                print("bob")
                win.fill((0,0,0))
                pause_font = pygame.font.SysFont("comicsans", 50)
                text = pause_font.render("Paused", 1, (255,255,255))
                pause = False


def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    rule_font = pygame.font.SysFont("comicsans", 40)
    run = True
    while run:
        win.blit(BG, (0,0))
        title_label = title_font.render("Press to begin...", 1, (255,255,255))
        # rules
        rules1 = rule_font.render("Use the arrow keys to move your player.", 1, (255,255,255))
        rules2 = rule_font.render("Use the space bar to shoot your enemy ", 1, (255,255,255))
        rules3 = rule_font.render("before they reach the end of the line.", 1, (255,255,255))
        rules4 = rule_font.render("Mind that you hava a health bar.", 1, (255,255,255))
        win.blit(rules1, (WIDTH/2 - rules1.get_width()/2, 450))
        win.blit(rules2, (WIDTH/2 - rules2.get_width()/2, 480))
        win.blit(rules3, (WIDTH/2 - rules3.get_width()/2, 510))
        win.blit(rules4, (WIDTH/2 - rules3.get_width()/2, 540))

        win.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                main()
    pygame.quit()


main_menu()