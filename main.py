import pygame
import random
import os

# --- 1. СТАРТ ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Trolleybus Tap Mobile FIXED")
clock = pygame.time.Clock()

folder = os.path.dirname(__file__)
img_path = os.path.join(folder, 'images')

def load_img(name, w, h):
    path = os.path.join(img_path, name)
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (w, h))
    except:
        return pygame.Surface((w, h))

# --- 2. БЕЗОПАСНЫЙ РЕКОРД ---
def load_record():
    try:
        path = os.path.join(folder, "record.txt")
        if os.path.exists(path):
            with open(path, "r") as f:
                return int(f.read())
    except: pass
    return 0

def save_record(score):
    try:
        path = os.path.join(folder, "record.txt")
        with open(path, "w") as f:
            f.write(str(score))
    except Exception as e:
        print(f"Ошибка сохранения: {e}")

# Загрузка
trolley_img = load_img('item.png', 120, 80)
map1 = load_img('bg_tashkent.png', WIDTH, HEIGHT)
map2 = load_img('bg_space.png', WIDTH, HEIGHT)

score = 0
high_score = load_record()
bus_x, bus_y = 300, 200
active_bg = None
state = 0 

# --- 3. ЦИКЛ ---
running = True
while running:
    clock.tick(144)
    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if state == 0:
                if 200 < my < 400:
                    if 50 < mx < 350:
                        active_bg, state, score = map1, 1, 0
                    elif 450 < mx < 750:
                        active_bg, state, score = map2, 1, 0
            
            elif state == 1:
                # ПРОВЕРКА ТАПА ПО ТРОЛЛЕЙБУСУ
                if bus_x < mx < bus_x + 120 and bus_y < my < bus_y + 80:
                    score += 1
                    bus_x, bus_y = random.randint(50, 650), random.randint(50, 450)
                    if score > high_score:
                        high_score = score
                        save_record(high_score) # Теперь это безопасно!
                
                # EXIT
                if 700 < mx < 790 and 10 < my < 60:
                    state = 0

    # --- 4. РИСОВАНИЕ ---
    if state == 0:
        screen.fill((20, 20, 40))
        font = pygame.font.SysFont(None, 60)
        pygame.draw.rect(screen, (50, 80, 150), (50, 200, 300, 200), border_radius=15)
        pygame.draw.rect(screen, (120, 50, 150), (450, 200, 300, 200), border_radius=15)
        screen.blit(font.render("TASHKENT", True, (255, 255, 255)), (85, 280))
        screen.blit(font.render("SPACE", True, (255, 255, 255)), (540, 280))
        screen.blit(font.render(f"BEST: {high_score}", True, (255, 215, 0)), (WIDTH//2 - 100, 450))

    elif state == 1:
        screen.blit(active_bg, (0, 0))
        screen.blit(trolley_img, (bus_x, bus_y))
        pygame.draw.rect(screen, (200, 50, 50), (700, 10, 90, 50), border_radius=10)
        screen.blit(pygame.font.SysFont(None, 30).render("EXIT", True, (255, 255, 255)), (720, 25))
        screen.blit(pygame.font.SysFont(None, 45).render(f"SCORE: {score}", True, (255, 255, 255)), (20, 20))

    pygame.display.flip()
pygame.quit()