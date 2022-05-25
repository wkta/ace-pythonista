import random

import pygame

import event


# body
# manager = event.EventManager.instance()
gameover = False
pygame.init()

clock = pygame.time.Clock()
SCR_W, SCR_H = 800, 600
scr_w = SCR_W
scr_h = SCR_H

screen = pygame.display.set_mode((SCR_W, SCR_H))
ft = pygame.font.Font(None, 33)
# - create the list of guys
NB_GUYS = 100

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
    
    def random_walk(self):
        self.pos[0] += random.randint(-4, 4)
        self.pos[1] += random.randint(-6, 6)
        if not (( 0< self.pos[0] <scr_w) and (0<self.pos[1]<scr_h)):
            self.pos[0] = 300
            self.pos[1] = 250


full_list = list()
for g, pos in sprite2pos.items():
    full_list.append(Guy(pos, g))

cpt = 0
manufps = 0
accu = 0
last_t = pygame.time.get_ticks()
lbl = None


def paint():
    global gameover, screen, full_list, lbl
    screen.fill('orange')
    pygame.draw.rect(screen, 'blue', (88, 33, 128, 250))
    pygame.draw.rect(screen, 'yellow', (22, 35, 200, 128))
    pygame.draw.circle(screen, 'red', (442, 238), 167)
    
    for e in full_list:
        screen.blit(e.surf, e.pos)
    screen.blit(lbl, (32, 32))
    pygame.display.flip()


def no_event_manager():
    global gameover, cpt, manufps, accu, last_t, lbl
    print('gameloop NO evt manager')
    # - GAME LOOP
    while not gameover:
        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                gameover = True
        
        lbl = ft.render(str(manufps), True, (0, 0, 0))

        # update positions
        for e in full_list:
            e.random_walk()
        
        # display
        paint()
        
        cpt += 1

        clock.tick_busy_loop()

        tnow = pygame.time.get_ticks()
        accu += (tnow - last_t)
        last_t = tnow
        if cpt > 256:
            manufps = cpt / (accu/1000)
            cpt = accu = 0

    pygame.quit()




class GameCtrl(event.Listener):
    def proc_event(self, ev):
        global gameover
        if ev.type == pygame.QUIT:
            gameover = True
        elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
            gameover = True
        elif ev.type == 111:
            # trigger refresh screen
            paint()


def with_event_manager():
    global gameover, cpt, manufps, accu, last_t, lbl
    # - GAME LOOP
    manager = event.EventManager.instance()
    manager.alien_ev_provider = pygame.event.get
    gctrl = GameCtrl()
    gctrl.turn_on()
    print('gameloop MANAGER is here')
    
    while not gameover:
        # events
        # see the .update below...
        
        lbl = ft.render(str(manufps), True, (0, 0, 0))

        # update positions
        for e in full_list:
            e.random_walk()
        full_list[-1].pev(111)  # paint-like
        
        manager.update()
        
        cpt += 1

        clock.tick_busy_loop()

        tnow = pygame.time.get_ticks()
        accu += (tnow - last_t)
        last_t = tnow
        if cpt > 256:
            manufps = cpt / (accu/1000)
            cpt = accu = 0

    pygame.quit()


print('with manager or without? ')
choice = int(input('1 or 0?'))
if choice:
    with_event_manager()
else:
    no_event_manager()
