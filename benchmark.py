import random
import time

import katagames_sdk as katasdk


katasdk.bootstrap()

kengi = katasdk.kengi
pygame = kengi.pygame

cpt = 0
ct = None
last_t = None
ft = None
manu_fps = None
manager = None
gameover = False
scr_w, scr_h = None, None
clock = pygame.time.Clock()
screen = None
guys = None
full_list = None
view = None
NB_GUYS = 122


class Guy(kengi.event.CogObj):  # event.Emitter
    def __init__(self, givenpos, surf):
        super().__init__()
        self.pos = givenpos
        self.surf = surf

    def randomwalk(self):
        self.pos[0] += random.randint(-4, 4)
        self.pos[1] += random.randint(-6, 6)
        self.pev(8238129, x=self.pos[0], y=self.pos[1], surf=self.surf)


class PseudoView(kengi.event.EventReceiver):  # event.Listener):
    def __init__(self):
        super().__init__()
        self.tempscr = pygame.Surface((scr_w, scr_h))
        self.tempscr.fill('orange')
        self.lbl = None

    def proc_event(self, ev, src):
        if ev.type == 8238129:
            self.tempscr.blit(ev.surf, (ev.x, ev.y))
        elif ev.type == 111:  # paint
            #screen.blit(self.tempscr, (0, 0))
            #screen.blit(self.lbl, (32, 32))
            #self.tempscr.fill('orange')
            screen.fill('blue')
            pygame.draw.rect(screen, 'black', (87, 15, 32, 32))
            screen.blit(self.lbl, (40, 40))


@katasdk.web_entry_point
def game_enter(vmstate=None):
    global scr_w, scr_h, screen, ft, full_list, view, manager
    kengi.init('hd')
    screen = kengi.get_surface()
    scr_w, scr_h = screen.get_size()
    ft = pygame.font.Font(None, 33)
    guys = [pygame.Surface((25, 25)) for _ in range(NB_GUYS)]
    omega = list(pygame.color.THECOLORS.keys())
    for g in guys:
        chosen_k = random.choice(omega)
        g.fill(pygame.color.THECOLORS[chosen_k])
    sprite2pos = dict()
    for g in guys:
        sprite2pos[g] = [random.randint(0, scr_w), random.randint(0, scr_h)]

    full_list = list()
    for g, pos in sprite2pos.items():
        full_list.append(Guy(pos, g))

    view = PseudoView()
    view.turn_on()
    manager = kengi.event.EventManager.instance()
    print(' -- fin init --')


@katasdk.web_animate
def game_update(tinfo=None):
    global manu_fps, cpt, view, full_list, gameover, ft, full_list, last_t, ct

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover = True

    ct = time.time()

    if last_t is None:
        last_t = ct
    elif ct - last_t > 2.1:
        delta = ct - last_t
        last_t = ct
        manu_fps = cpt / (delta)
        cpt = 0

    # view.lbl = ft.render(str(round(clock.get_fps(), 2)), True, (0, 0, 0))
    view.lbl = ft.render(str(manu_fps), True, (0, 0, 0))

    # update positions
    for e in full_list:
        e.randomwalk()
    full_list[-1].pev(111)  # fake paint event
    manager.update()

    # display
    cpt += 1
    kengi.flip()


if __name__ == '__main__':
    game_enter(None)
    while not gameover:
        game_update()
    kengi.quit()
