import pygame
import time

pygame.init()

x = 1280
y = 720
screen = pygame.display.set_mode((x, y))
run = True
pygame.display.set_caption("my game")

class Enemys:
    def __init__(self, player):
        self.width = 50
        self.height = 50
        self.enemys = []
        self.velocity = 10
        self.margin = 7
        self.player = player
        self.enemycount = 3

    def draw(self):
        if len(self.enemys) == 0:
            self.create(self.enemycount)
            self.enemycount += 1
            self.velocity += 0.2
            self.player.shot_time -= 0.01
            self.player.shootVelocity += 0.1
            self.player.velocity += 0.2
        self.IsDeath()
        self.IsKill()
        for i, item in enumerate(self.enemys):
            if item['side'] == 'left':
                item['x'] += self.velocity
            else:
                item['x'] -= self.velocity
            if item['x'] >= screen.get_width() - self.width:
                item['y'] += self.height + self.margin
                item['x'] -= self.margin
                item['side'] = 'right'
            if item['x'] <= 0:
                item['y'] += self.height + self.margin
                item['x'] += self.margin
                item['side'] = 'left'
            pygame.draw.rect(screen, 'yellow', (item['x'], item['y'], self.width, self.height))
    def IsKill(self):
        for i,item in enumerate(self.enemys):
            if (item['x'] <= self.player.pos['x'] <= self.player.pos['x'] + self.width
                    and item['y'] <= self.player.pos['y'] <= item['y'] + self.height):
                self.player.pos['x'] = screen.get_width() / 2 - self.width / 2
                self.player.shoots = []
                self.enemys = []
                self.enemycount = 3
    def IsDeath(self):
        for i, enemy_ in enumerate(self.enemys):
            for i2, shoot_ in enumerate(self.player.shoots):
                if (enemy_['x'] <= shoot_['x'] <= enemy_['x'] + self.width
                        and enemy_['y'] <= shoot_['y'] <= enemy_['y'] + self.height):
                    self.player.shoots.pop(i2)
                    self.enemys.pop(i)
                    self.player.last_shot_time = 0
                    self.player.shot_time = 0.6
                    self.player.shootOn = True

    def create(self, count):
        lastenemy = 0
        column = -105
        for _ in range(count):
            if lastenemy + self.width >= screen.get_width() - self.width:
                column += self.height + self.margin
                lastenemy = 0
            temp_enemy = {
                'x': lastenemy + self.width,
                'y': self.height + column,
                'side': 'left'
            }
            lastenemy += self.width + self.margin
            self.enemys.append(temp_enemy)


class Player:
    def __init__(self):
        self.pos = dict(x=0, y=0)
        self.pos['y'] = screen.get_height() - 100
        self.velocity = 12
        self.width = 50
        self.height = 50
        self.pos['x'] = screen.get_width() / 2 - self.width / 2
        self.shoots = []
        self.keys = pygame.key.get_pressed()
        self.last_shot_time = 0
        self.shot_time = 1.7
        self.shootOn = True
        self.shootVelocity = 12

    def draw(self):
        self.keys = pygame.key.get_pressed()
        pygame.draw.rect(screen, 'red', (self.pos['x'], self.pos['y'], self.width, self.height))
        self.move()
        self.collision()
        self.shoot()
        self.drawshoots()

    def shoot(self):
        if self.keys[pygame.K_w] and self.shootOn:
            temp_shoot = {
                'x': self.pos['x'] + self.width / 2,
                'y': self.pos['y']
            }
            self.shoots.append(temp_shoot)
            self.shootOn = False
        current_time = time.time()
        if current_time - self.last_shot_time >= self.shot_time:
            if not self.shootOn:
                self.shootOn = True
            self.last_shot_time = current_time

    def drawshoots(self):
        for i, item in enumerate(self.shoots):
            if item['y'] <= 0 - self.height:
                self.shoots.pop(i)
            item['y'] -= self.shootVelocity
            pygame.draw.rect(screen, 'blue', (item['x'], item['y'], 5, 10))

    def move(self):
        if self.keys[pygame.K_a] or self.keys[pygame.K_LEFT]:
            self.pos['x'] -= self.velocity
        elif self.keys[pygame.K_d] or self.keys[pygame.K_RIGHT]:
            self.pos['x'] += self.velocity

    def collision(self):
        if self.pos['x'] <= 0:
            self.pos['x'] = 0
        if self.pos['x'] >= screen.get_width() - self.width:
            self.pos['x'] = screen.get_width() - self.height


player1 = Player()
enemy = Enemys(player1)


def main():
    screen.fill('black')
    player1.draw()
    enemy.draw()


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    main()
    pygame.display.flip()
