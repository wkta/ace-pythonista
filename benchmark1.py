import random

import pygame

import event


# body
cpt = 0
last_t = manu_fps = None
manager = event.EventManager.instance()
gameover = False
clock = pygame.time.Clock()
pygame.init()
SCR_W, SCR_H = 800, 600
screen = pygame.display.set_mode((SCR_W, SCR_H))
ft = pygame.font.Font(None, 33)
# - create the list of guys
NB_GUYS = 122
guys = [pygame.Surface((25, 25)) for _ in range(NB_GUYS)]
omega = list(pygame.color.THECOLORS.keys())
for g in guys:
    chosen_k = random.choice(omega)
    g.fill(pygame.color.THECOLORS[chosen_k])
sprite2pos = dict()
for g in guys:
    sprite2pos[g] = [random.randint(0, SCR_W), random.randint(0, SCR_H)]


class Guy(event.Emitter):
    def __init__(self, givenpos, surf):
        super().__init__()
        self.pos = givenpos
        self.surf = surf


full_list = list()
for g, pos in sprite2pos.items():
    full_list.append(Guy(pos, g))


while not gameover:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover = True

    ct = pygame.time.get_ticks()
    if last_t is None:
        last_t = ct
    elif ct - last_t > 850:
        delta = ct - last_t
        last_t = ct
        manu_fps = cpt / (delta/1000)
        cpt = 0

    lbl = ft.render(str(manu_fps), True, (0, 0, 0))

    # update positions
    for e in full_list:
        e.pos[0] += random.randint(-4, 4)
        e.pos[1] += random.randint(-6, 6)

    # display
    screen.fill('orange')
    for e in full_list:
        screen.blit(e.surf, e.pos)
    screen.blit(lbl, (32, 32))
    cpt += 1
    pygame.display.flip()
    clock.tick_busy_loop()

pygame.quit()
print('done.')
