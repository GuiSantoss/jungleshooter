import pgzrun, sys
import os
from pygame import Rect, transform

# --- CONFIGURAÇÕES ---
WIDTH, HEIGHT, TITLE = 800, 600, "Jungle Shooter - Final"
GRAVITY, JUMP, SPEED = 0.8, -14, 5

print("\n--- VERIFICAÇÃO DE ARQUIVOS ---")
if os.path.exists('music/music.mp3'): print("OK: music/music.mp3 encontrado!")
elif os.path.exists('music/music.ogg'): print("OK: music/music.ogg encontrado!")
else: print("AVISO: Verifique se moveu a música para a pasta 'music'!")
print("-------------------------------\n")

# --- CLASSES ---
class Bullet:
    def __init__(self, x, y, direction):
        self.rect = Rect(x, y, 10, 6)
        self.vx = 6 * direction
        self.active = True
    def update(self):
        self.rect.x += self.vx
        if not (0 < self.rect.centerx < WIDTH): self.active = False
    def draw(self): screen.draw.filled_rect(self.rect, "yellow")

class Entity(Actor):
    def __init__(self, idle_imgs, walk_imgs, x, y):
        super().__init__(idle_imgs[0], pos=(x, y))
        self.imgs_idle, self.imgs_walk = idle_imgs, walk_imgs
        self.timer, self.frame = 0, 0
        self.vy, self.grounded = 0, False
        self.alive, self.moving = True, False
        self.direction = 1 # 1 = Direita, -1 = Esquerda

    def apply_physics(self, platforms):
        self.vy += GRAVITY
        self.y += self.vy
        self.grounded = False
        for plat in platforms:
            if self.colliderect(plat) and self.vy > 0:
                if self.bottom - self.vy <= plat.top + 15:
                    self.bottom = plat.top; self.vy = 0; self.grounded = True
        if self.top > HEIGHT: self.alive = False

    def animate(self, dt):
        self.timer += dt
        frames, interval = (self.imgs_walk, 0.15) if self.moving else (self.imgs_idle, 0.4)
        if self.timer > interval:
            self.frame = (self.frame + 1) % len(frames)
            self.image = frames[self.frame]
            self.timer = 0
            
    def draw(self):
        # Se a imagem original olha para ESQUERDA, invertemos a lógica:
        # Quando direction == 1 (Direita), nós espelhamos (Flip).
        if self.direction == 1:
            flipped_img = transform.flip(self._surf, True, False)
            screen.blit(flipped_img, self.topleft)
        else:
            super().draw()

class Hero(Entity):
    def update(self, platforms, dt):
        self.moving = False
        if keyboard.left:  
            self.x -= SPEED
            self.moving = True
            self.direction = -1 
        if keyboard.right: 
            self.x += SPEED
            self.moving = True
            self.direction = 1  
            
        self.apply_physics(platforms)
        self.animate(dt)
        self.left = max(0, self.left); self.right = min(WIDTH, self.right)

    def jump(self):
        if self.grounded:
            self.vy = JUMP
            try: sounds.jump.play()
            except: pass

class Enemy(Entity):
    def __init__(self, x, y, dist):
        super().__init__(['enemy_idle_1'], ['enemy_idle_2'], x, y)
        self.start_x, self.max_dist = x, dist
        self.direction = 1 
        self.shoot_timer = 0
        self.moving = True

    def update(self, platforms, bullets, dt):
        self.apply_physics(platforms)
        
        # Movimento
        self.x += 2 * self.direction
        if abs(self.x - self.start_x) > self.max_dist: 
            self.direction *= -1
        
        # Tiro
        self.shoot_timer += dt
        if self.shoot_timer > 2.0: 
            # Se a imagem é invertida, o tiro deve sair
            bullets.append(Bullet(self.x, self.y - 10, self.direction))
            self.shoot_timer = 0
        self.animate(dt)

# --- GERENCIADOR DO JOGO ---
class Game:
    def __init__(self):
        self.state, self.sound = 'MENU', True
        self.btns = [Actor('button', center=(WIDTH/2, y)) for y in (250, 350, 450)]
        self.reset()

    def create_row(self, x, y, blocks):
        return [Actor('ground', topleft=(x + (i * 40), y)) for i in range(blocks)]

    def reset(self):
        self.hero = Hero(['hero_idle_1', 'hero_idle_2'], ['hero_walk_1', 'hero_walk_2'], 50, 500)
        self.bullets = []
        self.plats = []

        level_data = [
            (200, 500, 3), (450, 450, 4),   
            (100, 380, 3), (300, 320, 2),   
            (500, 300, 4), (700, 250, 2),   
            (450, 180, 3), (250, 150, 4),   
            (50, 100, 3)                    
        ]

        for p in level_data:
            self.plats += self.create_row(p[0], p[1], p[2])
        
        self.plats += self.create_row(0, HEIGHT-40, 20)

        try: self.goal = Actor('goal', topleft=(60, 40))
        except: self.goal = Actor('button', topleft=(60, 40))

        self.enemies = [
            Enemy(400, 500, 100), Enemy(500, 450, 50), 
            Enemy(140, 380, 30), Enemy(550, 300, 50), 
            Enemy(300, 150, 50), Enemy(80, 100, 20)
        ]
        
        if self.sound: self.music_ctrl(True)

    def music_ctrl(self, play):
        if play:
            try:
                if not music.is_playing('music'):
                    music.play('music')
            except: pass
        else:
            music.stop()

    def update(self, dt):
        if self.state == 'GAME':
            self.hero.update(self.plats, dt)
            if self.hero.colliderect(self.goal): self.state = 'WIN'
            if not self.hero.alive: self.state = 'GAMEOVER'

            for e in self.enemies:
                e.update(self.plats, self.bullets, dt)
                if self.hero.colliderect(e): self.hero.alive = False

            for b in self.bullets:
                b.update()
                if b.active and self.hero.colliderect(b.rect): self.hero.alive = False
            self.bullets = [b for b in self.bullets if b.active]

    def draw(self):
        screen.clear()
        if self.state == 'MENU':
            screen.fill((30, 30, 40))
            screen.draw.text("JUNGLE SHOOTER", center=(WIDTH/2, 100), fontsize=60, color="white")
            
            labels = ["JOGAR", f"SOM: {self.sound}", "SAIR"]
            for btn, txt in zip(self.btns, labels):
                btn.draw()
                screen.draw.text(txt, center=(btn.x, btn.y + 35), fontsize=25, color="white", shadow=(1,1))

        elif self.state == 'GAME':
            screen.fill((146, 244, 255)) 
            self.goal.draw(); self.hero.draw()
            for obj in self.plats + self.enemies + self.bullets: obj.draw()

        else: 
            screen.fill("black")
            msg = "VITÓRIA!" if self.state == 'WIN' else "GAME OVER"
            color = "green" if self.state == 'WIN' else "red"
            screen.draw.text(msg, center=(WIDTH/2, HEIGHT/2), fontsize=80, color=color)
            screen.draw.text("[ESPAÇO] Menu", center=(WIDTH/2, HEIGHT/2+60), fontsize=30, color="white")

    def click(self, pos):
        if self.state == 'MENU':
            if self.btns[0].collidepoint(pos): self.state = 'GAME'; self.reset()
            elif self.btns[1].collidepoint(pos): 
                self.sound = not self.sound
                self.music_ctrl(self.sound)
            elif self.btns[2].collidepoint(pos): sys.exit()

    def key(self, k):
        if self.state == 'GAME' and k == keys.SPACE: self.hero.jump()
        elif self.state in ('WIN', 'GAMEOVER') and k == keys.SPACE: self.state = 'MENU'


game = Game()
def update(dt): game.update(dt)
def draw(): game.draw()
def on_mouse_down(pos): game.click(pos)
def on_key_down(key): game.key(key)

pgzrun.go()