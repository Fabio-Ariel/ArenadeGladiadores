# -*- coding: utf-8 -*-
import pgzrun
import random
from pygame import Rect

WIDTH = 960
HEIGHT = 590

# Estados do jogo
MENU = 0
PLAYING = 1
GAME_OVER = 2
VICTORY = 3

game_state = MENU

# Sistema de audio
sound_enabled = True

# Sistema de fases
current_phase = 1
kills_count = 0
PHASE_GOALS = {1: 10, 2: 15, 3: 20}
PHASE_BACKGROUNDS = {
    1: "cenario/coliseu_resized1",
    2: "cenario/coliseu_resized",
    3: "cenario/coliseu_resized2"
}

# Definir limites da arena (circulo de areia)
ARENA_CENTER_X = WIDTH // 2
ARENA_CENTER_Y = 320
ARENA_RADIUS = 280

# Posicoes das portas (zonas permitidas para entrada)
DOOR_ZONES = [
    {'x': WIDTH // 2, 'y': 100, 'radius': 40},
    {'x': WIDTH // 2 - 200, 'y': 150, 'radius': 40},
    {'x': WIDTH // 2 + 200, 'y': 150, 'radius': 40},
    {'x': WIDTH // 2 - 250, 'y': 200, 'radius': 40},
]

def is_in_door_zone(x, y):
    """Verifica se esta em uma zona de porta"""
    for door in DOOR_ZONES:
        dist = ((x - door['x']) ** 2 + (y - door['y']) ** 2) ** 0.5
        if dist <= door['radius']:
            return True
    return False

# Classe para gerenciar animacoes
class AnimatedCharacter:
    def __init__(self, x, y, speed=3, is_enemy=False):
        self.x = x
        self.y = y
        self.speed = speed
        self.current_animation = "idle"
        self.direction = "right"
        self.frame = 1
        self.frame_counter = 0
        self.idle_delay = 15
        self.walk_delay = 6
        self.attack_delay = 4
        self.is_attacking = False
        self.is_enemy = is_enemy
        self.actor = Actor("idleright/gladiador_idle_right1")
        self.actor.pos = (x, y)
        self.has_dealt_damage = False
        
        if is_enemy:
            self.hp = 2
            self.damage = 1
            self.target_x = ARENA_CENTER_X
            self.target_y = ARENA_CENTER_Y
            self.ai_counter = 0
            self.attack_cooldown = 0
        else:
            self.hp = 100
            self.max_hp = 100
            self.damage = 1
    
    def take_damage(self, damage):
        """Recebe dano"""
        self.hp -= damage
        if self.is_enemy and self.hp > 0:
            if sound_enabled:
                try:
                    sounds.young_man_being_hurt.play()
                except:
                    pass
        return self.hp <= 0
    
    def get_current_delay(self):
        """Retorna o delay apropriado para a animacao atual"""
        if self.current_animation == "idle":
            return self.idle_delay
        elif self.current_animation == "attack":
            return self.attack_delay
        else:
            return self.walk_delay
        
    def animate(self):
        """Atualiza a animacao"""
        current_delay = self.get_current_delay()
        
        self.frame_counter += 1
        
        if self.frame_counter >= current_delay:
            self.frame_counter = 0
            self.frame += 1
            
            if self.current_animation == "attack":
                if self.frame == 5:
                    self.has_dealt_damage = False
                elif self.frame == 6:
                    self.has_dealt_damage = True
                
                if self.frame > 9:
                    self.is_attacking = False
                    self.has_dealt_damage = True
                    self.set_animation("idle")
                    return
                
                if self.direction == "left":
                    self.actor.image = f"attackleft/gladiador_attack_left{self.frame}"
                else:
                    self.actor.image = f"attackright/gladiador_attack_right{self.frame}"
            
            elif self.current_animation == "idle":
                if self.frame > 3:
                    self.frame = 1
                if self.direction == "left":
                    self.actor.image = f"idleleft/gladiador_idle_left{self.frame}"
                else:
                    self.actor.image = f"idleright/gladiador_idle_right{self.frame}"
            
            elif self.current_animation == "walk_right":
                if self.frame > 6:
                    self.frame = 1
                self.actor.image = f"walkright/gladiador_walk_right{self.frame}"
            
            elif self.current_animation == "walk_left":
                if self.frame > 6:
                    self.frame = 1
                self.actor.image = f"walkleft/gladiador_walk_left{self.frame}"
            
            elif self.current_animation == "walk_vertical":
                if self.frame > 6:
                    self.frame = 1
                if self.direction == "left":
                    self.actor.image = f"walkleft/gladiador_walk_left{self.frame}"
                else:
                    self.actor.image = f"walkright/gladiador_walk_right{self.frame}"
    
    def move(self, dx, dy):
        """Move o personagem"""
        new_x = self.x + dx
        new_y = self.y + dy
        
        dist_from_center = ((new_x - ARENA_CENTER_X) ** 2 + (new_y - ARENA_CENTER_Y) ** 2) ** 0.5
        
        if dist_from_center <= ARENA_RADIUS or is_in_door_zone(new_x, new_y):
            self.x = new_x
            self.y = new_y
            self.actor.pos = (self.x, self.y)
        elif self.is_enemy:
            old_dist = ((self.x - ARENA_CENTER_X) ** 2 + (self.y - ARENA_CENTER_Y) ** 2) ** 0.5
            if dist_from_center < old_dist:
                self.x = new_x
                self.y = new_y
                self.actor.pos = (self.x, self.y)
    
    def set_animation(self, animation_name):
        """Muda a animacao"""
        if self.current_animation != animation_name:
            self.current_animation = animation_name
            self.frame = 1
            self.frame_counter = 0
    
    def attack(self):
        """Inicia o ataque"""
        if not self.is_attacking:
            self.is_attacking = True
            self.has_dealt_damage = False
            self.set_animation("attack")
            if sound_enabled:
                try:
                    sounds.sword_slice.play()
                except:
                    pass
            return True
        return False
    
    def get_attack_range(self):
        """Retorna a area de ataque do personagem"""
        attack_distance = 60
        attack_height = 60
        
        if self.direction == "left":
            return (self.x - attack_distance, self.y - attack_height // 2, 
                   self.x, self.y + attack_height // 2)
        else:
            return (self.x, self.y - attack_height // 2, 
                   self.x + attack_distance, self.y + attack_height // 2)
    
    def is_in_attack_range(self, other):
        """Verifica se outro personagem esta no alcance do ataque"""
        if not self.is_attacking or self.frame != 5 or self.has_dealt_damage:
            return False
        
        x1, y1, x2, y2 = self.get_attack_range()
        return x1 <= other.x <= x2 and y1 <= other.y <= y2
    
    def enemy_ai(self, player):
        """IA simples para inimigos"""
        if self.is_attacking:
            return
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        self.ai_counter += 1
        
        dist_to_player = ((self.x - player.x) ** 2 + (self.y - player.y) ** 2) ** 0.5
        
        if dist_to_player < 120 and self.attack_cooldown == 0:
            if player.x < self.x:
                self.direction = "left"
            else:
                self.direction = "right"
            
            self.attack()
            self.attack_cooldown = 90
            return
        
        if self.ai_counter >= 60:
            self.ai_counter = 0
            
            dist_from_center = ((self.x - ARENA_CENTER_X) ** 2 + (self.y - ARENA_CENTER_Y) ** 2) ** 0.5
            
            if dist_from_center > ARENA_RADIUS and not is_in_door_zone(self.x, self.y):
                self.target_x = ARENA_CENTER_X
                self.target_y = ARENA_CENTER_Y
            else:
                self.target_x = player.x
                self.target_y = player.y
        
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = (dx**2 + dy**2) ** 0.5
        
        if dist > 5:
            dx = (dx / dist) * self.speed * 0.7
            dy = (dy / dist) * self.speed * 0.7
            
            if abs(dx) > abs(dy):
                if dx > 0:
                    self.direction = "right"
                    self.set_animation("walk_right")
                else:
                    self.direction = "left"
                    self.set_animation("walk_left")
            else:
                self.set_animation("walk_vertical")
            
            self.move(dx, dy)
        else:
            self.set_animation("idle")

DOOR_POSITIONS = [
    (WIDTH // 2, 100),
    (WIDTH // 2 - 200, 150),
    (WIDTH // 2 + 200, 150),
    (WIDTH // 2 - 250, 200),
]

player = None
enemies = []

def spawn_enemy():
    """Cria um novo inimigo em uma porta aleatoria"""
    door_pos = random.choice(DOOR_POSITIONS)
    enemy = AnimatedCharacter(door_pos[0], door_pos[1], speed=2, is_enemy=True)
    enemies.append(enemy)

def start_game():
    """Inicia um novo jogo"""
    global player, enemies, game_state, current_phase, kills_count
    player = AnimatedCharacter(WIDTH // 2, HEIGHT - 150)
    enemies = []
    current_phase = 1
    kills_count = 0
    for i in range(3):
        spawn_enemy()
    game_state = PLAYING
    if sound_enabled:
        try:
            music.play('somjogo')
        except:
            pass

def next_phase():
    """Avanca para a proxima fase"""
    global current_phase, kills_count, enemies
    current_phase += 1
    kills_count = 0
    enemies = []
    
    player.hp = min(player.hp + 30, player.max_hp)
    
    for i in range(3):
        spawn_enemy()

def draw():
    if game_state == MENU:
        screen.blit("cenario/coliseu_resized", (0, 0))
        
        screen.draw.text("ARENA DE GLADIADORES", 
                        center=(WIDTH // 2, HEIGHT // 2 - 150), 
                        color="white", fontsize=50)
        
        screen.draw.filled_rect(
            Rect(WIDTH // 2 - 100, HEIGHT // 2 - 40, 200, 50), 
            color="darkred"
        )
        screen.draw.text("INICIAR JOGO", 
                        center=(WIDTH // 2, HEIGHT // 2 - 15), 
                        color="white", fontsize=30)
        
        sound_text = "SOM: LIGADO" if sound_enabled else "SOM: DESLIGADO"
        sound_color = "darkgreen" if sound_enabled else "darkgray"
        screen.draw.filled_rect(
            Rect(WIDTH // 2 - 100, HEIGHT // 2 + 30, 200, 50), 
            color=sound_color
        )
        screen.draw.text(sound_text, 
                        center=(WIDTH // 2, HEIGHT // 2 + 55), 
                        color="white", fontsize=30)
        
        screen.draw.filled_rect(
            Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50), 
            color="gray"
        )
        screen.draw.text("SAIR", 
                        center=(WIDTH // 2, HEIGHT // 2 + 125), 
                        color="white", fontsize=30)
        
        screen.draw.text("Use as SETAS para mover", 
                        center=(WIDTH // 2, HEIGHT // 2 + 170), 
                        color="white", fontsize=20)
        screen.draw.text("Aperte ESPACO para atacar", 
                        center=(WIDTH // 2, HEIGHT // 2 + 200), 
                        color="white", fontsize=20)
    
    elif game_state == PLAYING:
        screen.blit(PHASE_BACKGROUNDS[current_phase], (0, 0))
        
        for enemy in enemies:
            enemy.actor.draw()
        
        player.actor.draw()
        
        screen.draw.text(f"HP: {player.hp}/{player.max_hp}", 
                        (10, 10), color="white", fontsize=30)
        screen.draw.text(f"Fase: {current_phase}/3", 
                        (10, 40), color="white", fontsize=30)
        screen.draw.text(f"Mortes: {kills_count}/{PHASE_GOALS[current_phase]}", 
                        (10, 70), color="white", fontsize=30)
        
        bar_width = 200
        bar_height = 20
        hp_percentage = player.hp / player.max_hp
        screen.draw.filled_rect(
            Rect(10, 100, bar_width, bar_height), 
            color="red"
        )
        screen.draw.filled_rect(
            Rect(10, 100, int(bar_width * hp_percentage), bar_height), 
            color="green"
        )
    
    elif game_state == GAME_OVER:
        screen.blit("cenario/coliseu_resized", (0, 0))
        
        screen.draw.text("VOCE MORREU!", 
                        center=(WIDTH // 2, HEIGHT // 2 - 100), 
                        color="red", fontsize=60)
        
        screen.draw.filled_rect(
            Rect(WIDTH // 2 - 120, HEIGHT // 2, 240, 50), 
            color="darkred"
        )
        screen.draw.text("TENTAR NOVAMENTE", 
                        center=(WIDTH // 2, HEIGHT // 2 + 25), 
                        color="white", fontsize=30)
        
        screen.draw.filled_rect(
            Rect(WIDTH // 2 - 120, HEIGHT // 2 + 70, 240, 50), 
            color="gray"
        )
        screen.draw.text("MENU PRINCIPAL", 
                        center=(WIDTH // 2, HEIGHT // 2 + 95), 
                        color="white", fontsize=30)
    
    elif game_state == VICTORY:
        screen.blit(PHASE_BACKGROUNDS[3], (0, 0))
        
        screen.draw.text("VITORIA!", 
                        center=(WIDTH // 2, HEIGHT // 2 - 100), 
                        color="gold", fontsize=60)
        screen.draw.text("Voce completou todas as fases!", 
                        center=(WIDTH // 2, HEIGHT // 2 - 40), 
                        color="white", fontsize=30)
        
        screen.draw.filled_rect(
            Rect(WIDTH // 2 - 120, HEIGHT // 2 + 20, 240, 50), 
            color="darkred"
        )
        screen.draw.text("JOGAR NOVAMENTE", 
                        center=(WIDTH // 2, HEIGHT // 2 + 45), 
                        color="white", fontsize=30)
        
        screen.draw.filled_rect(
            Rect(WIDTH // 2 - 120, HEIGHT // 2 + 90, 240, 50), 
            color="gray"
        )
        screen.draw.text("MENU PRINCIPAL", 
                        center=(WIDTH // 2, HEIGHT // 2 + 115), 
                        color="white", fontsize=30)

def on_mouse_down(pos):
    """Detecta cliques do mouse"""
    global game_state, sound_enabled
    
    if game_state == MENU:
        if (WIDTH // 2 - 100 <= pos[0] <= WIDTH // 2 + 100 and 
            HEIGHT // 2 - 40 <= pos[1] <= HEIGHT // 2 + 10):
            start_game()
        
        elif (WIDTH // 2 - 100 <= pos[0] <= WIDTH // 2 + 100 and 
              HEIGHT // 2 + 30 <= pos[1] <= HEIGHT // 2 + 80):
            sound_enabled = not sound_enabled
            if not sound_enabled:
                try:
                    music.stop()
                except:
                    pass
        
        elif (WIDTH // 2 - 100 <= pos[0] <= WIDTH // 2 + 100 and 
              HEIGHT // 2 + 100 <= pos[1] <= HEIGHT // 2 + 150):
            exit()
    
    elif game_state == GAME_OVER:
        if (WIDTH // 2 - 120 <= pos[0] <= WIDTH // 2 + 120 and 
            HEIGHT // 2 <= pos[1] <= HEIGHT // 2 + 50):
            start_game()
        
        elif (WIDTH // 2 - 120 <= pos[0] <= WIDTH // 2 + 120 and 
              HEIGHT // 2 + 70 <= pos[1] <= HEIGHT // 2 + 120):
            game_state = MENU
            try:
                music.stop()
            except:
                pass
    
    elif game_state == VICTORY:
        if (WIDTH // 2 - 120 <= pos[0] <= WIDTH // 2 + 120 and 
            HEIGHT // 2 + 20 <= pos[1] <= HEIGHT // 2 + 70):
            start_game()
        
        elif (WIDTH // 2 - 120 <= pos[0] <= WIDTH // 2 + 120 and 
              HEIGHT // 2 + 90 <= pos[1] <= HEIGHT // 2 + 140):
            game_state = MENU
            try:
                music.stop()
            except:
                pass

def update():
    global enemies, game_state, kills_count
    
    if game_state != PLAYING:
        return
    
    if player.is_attacking:
        player.animate()
        
        if player.frame == 5 and not player.has_dealt_damage:
            for enemy in enemies[:]:
                if player.is_in_attack_range(enemy):
                    player.has_dealt_damage = True
                    if enemy.take_damage(player.damage):
                        enemies.remove(enemy)
                        kills_count += 1
                        
                        if kills_count >= PHASE_GOALS[current_phase]:
                            if current_phase < 3:
                                next_phase()
                            else:
                                game_state = VICTORY
                                try:
                                    music.stop()
                                except:
                                    pass
                    break
    else:
        moveu = False
        
        if keyboard.space:
            player.attack()
            return
        
        if keyboard.left:
            player.move(-player.speed, 0)
            player.set_animation("walk_left")
            player.direction = "left"
            moveu = True
        elif keyboard.right:
            player.move(player.speed, 0)
            player.set_animation("walk_right")
            player.direction = "right"
            moveu = True
        elif keyboard.up:
            player.move(0, -player.speed)
            player.set_animation("walk_vertical")
            moveu = True
        elif keyboard.down:
            player.move(0, player.speed)
            player.set_animation("walk_vertical")
            moveu = True
        
        if not moveu:
            player.set_animation("idle")
        
        player.animate()
    
    for enemy in enemies[:]:
        enemy.enemy_ai(player)
        enemy.animate()
        
        if enemy.frame == 5 and not enemy.has_dealt_damage:
            if enemy.is_in_attack_range(player):
                enemy.has_dealt_damage = True
                if player.take_damage(enemy.damage):
                    game_state = GAME_OVER
                    try:
                        music.stop()
                    except:
                        pass
    
    if len(enemies) < 3 and random.random() < 0.01:
        spawn_enemy()

pgzrun.go()
