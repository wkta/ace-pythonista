"""
modelize an event:
  use (evtype, {kwargs})

listener:
  when turned on -> auto-detects what events are supported,
  register on the manager unique object

event manager:
  should store
  {
    ev_t0 : [listener1, ...]
    ev_t1 : [listener2, ...]
  }
"""
import re

from structures.CircularBuffer import CircularBuffer
from structures.Singleton import Singleton

import pygame

# pygame.USEREVENT

FIRST_ENGIN_TYPE = pygame.USEREVENT

# new ideas(nov 22)
PseudoEnumSeed = lambda gt,c0: {i: ename for (i, ename) in zip(gt, range(c0,c0+len(gt)))}


class PseudoEnum:
    def __init__(self,seed):
        self._s = seed
    def __getattr__(self, name):
        return self._s[name]

      
def camel_case_format(string_ac_underscores):
    words = [word.capitalize() for word in string_ac_underscores.split('_')]
    return "".join(words)


def underscore_format(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


# ------------ construction d'enums -----------
def enum_builder_generic(to_upper, starting_index, *sequential, **named):
    domaine = range(starting_index, len(sequential) + starting_index)
    enums = dict(zip(sequential, domaine), **named)
    tmp_inv_map = {v: k for k, v in enums.items()}
    tmp_all_codes = domaine

    if to_upper:
        tmp = dict()
        for k, v in enums.items():
            if k == 'inv_map' or k == 'all_codes':
                continue
            tmp[k.upper()] = v
        enums = tmp

    enums['dict_repr'] = enums
    enums['inv_map'] = tmp_inv_map
    enums['all_codes'] = tmp_all_codes
    enums['last_code'] = len(sequential) + starting_index - 1
    enums['size'] = len(sequential)
    return type('Enum', (), enums)


def enum_from_n(n, *sequential, **named):
    return enum_builder_generic(False, n, *sequential, **named)


def enum(*sequential, **named):
    """
    the most used enum builder
    """
    return enum_from_n(0, *sequential, **named)
# ----------------- constr enums done ------------------------------------


def _enum_engine_ev_types(*sequential, **named):
    return enum_builder_generic(False, FIRST_ENGIN_TYPE, *sequential, **named)


EngineEvTypes = _enum_engine_ev_types(
    'Update',
    'Paint',
    # 'RefreshScreen',

    'Gamestart',  # correspond à l'ancien InitializeEvent
    'Gameover',  # indique que la sortie de jeu est certaine

    # 'BtClick',
    'ConvStart',  # contains convo_obj, portrait
    'ConvFinish',
    'ConvStep',  # contains value (used in rpgs like niobepolis, conv means conversation)

    'StateChange',  # contient un code state_ident
    'StatePush',  # contient un code state_ident
    'StatePop',

    #'FocusCh',
    #'FieldCh',
    #'DoAuth',

    'NetwSend',  # [num] un N°identification & [msg] un string (Async network comms)
    'NetwReceive'  # [num] un N°identification & [msg] un string (Async network comms)
)

first_custo_type = FIRST_ENGIN_TYPE + EngineEvTypes.size


def enum_ev_types(*sequential, **named):  # Custom events /!\ not engine events
    global first_custo_type
    # this function should be used by the custom game
    return enum_builder_generic(False, first_custo_type, *sequential, **named)


MyEvents = enum_ev_types(
    'TestEvent',
    'TestEventB'
)


@Singleton
class EventManager:
    def __init__(self):
        self._etype_to_listenerli = dict()
        self._cbuffer = CircularBuffer()
        self._known_ev_types = dict()  # corresp identifiant numérique <-> nom evenement
        self.regexp = None

    def post(self, etype, **kwargs):
        self._cbuffer.enqueue((etype, kwargs))

    def update(self):
        while len(self._cbuffer.deque_obj):
            # traiter event
            ev = self._cbuffer.dequeue()
            print(ev)

    def hard_reset(self):
        self._etype_to_listenerli.clear()
        self._cbuffer = CircularBuffer()
        self.event_types_inform()

    def _refresh_regexp(self, gnames):
        # we create a regexp such that, listeners know what keywords they have to consider
        # when analysing the list of their
        # .on_***
        # attribute methods
        regexp_prefix = '^on_(?:'
        rxp_body = '|'.join(gnames)
        regexp_sufix = '$)'
        print(regexp_prefix + rxp_body + regexp_sufix)
        self.regexp = re.compile(regexp_prefix + rxp_body + regexp_sufix)

    def register(self, ename, listener_obj):
        cod = EngineEvTypes.dict_repr[ename]
        if cod not in self._etype_to_listenerli:
            self._etype_to_listenerli[cod] = list()
        self._etype_to_listenerli[cod].append(listener_obj)

    def event_types_inform(self, given_ev_name_li=None):
        names = list()
        for eid, evname in EngineEvTypes.inv_map.items():
            names.append(underscore_format(evname))

        if given_ev_name_li:
            names.extend(given_ev_name_li)

        # force refresh regexp!
        self._refresh_regexp(names)


class KengiListenerObj:
    _free_listener_id = 34822

    def __init__(self):
        self._lid = self.__class__._free_listener_id
        self.__class__._free_listener_id += 1

        self._ev_manager_ref = None

        self._is_active = False
        self._inspection_res = set()

    def turn_on(self):
        if self._ev_manager_ref is None:
            self._ev_manager_ref = EventManager.instance()

        # introspection & detection des on_*
        # où * représente tout type d'évènement connu du moteur, que ce soit un event engine ou un event custom ajouté
        every_method = [method_name for method_name in dir(self) if callable(getattr(self, method_name))]
        callbacks_only = [mname for mname in every_method if self._ev_manager_ref.regexp.match(mname)]

        events_a_surveiller = list()
        for cbname in callbacks_only:
            # remove 'on_' prefix and convert Back to CamlCase
            events_a_surveiller.append(camel_case_format(cbname[3:]))
        print(events_a_surveiller)

        # enregistrement de son activité d'écoute auprès du evt manager
        for evname in events_a_surveiller:
            self._ev_manager_ref.register(evname, self)

    def turn_off(self):
        # opération contraire
        pass


class SampleListener(KengiListenerObj):
    def __init__(self, nom):
        super().__init__()
        self._avname = nom

    def get_av_name(self):
        return self._avname

    def set_av_name(self, x):
        self._avname = x

    def on_paint(self, ev):
        print('m1 -', ev)

    def on_lmao(self, ev):
        print('m1 -', ev)

    def on_update(self, ev):
        print('m2 -', ev)

    def on_netw_receive(self, ev):
        print('m3 -', ev)

    def __str__(self):
        return '<inst. Of SampleListener. Name='+str(self._avname)+'>'


# -----------------
#  testing
# ----------------
if __name__ == '__main__':
    manager = EventManager.instance()
    manager.event_types_inform()

    manager.post(17, serveur='api.gaudia-tech.com', machin='ouais')

    manager.post(3, jojo='trois', nom='tom')
    manager.post(551, hp='128', nom='roger')
    manager.post(17, hp='11', nom='jojo')
    manager.post(332, hp='59878', nom='poisson')

    print(manager._cbuffer.size())

    manager.update()
    print(manager._cbuffer.size())

    print(EngineEvTypes.Update)
    print(EngineEvTypes.Paint)
    print(MyEvents.TestEvent)
    print(MyEvents.TestEventB)

    # liste_brute = [
    #     '__init__',
    #     'machin',
    #     'on_paint',
    #     'truc',
    #     'on_update',
    #     'set_thing',
    #     'get_thing'
    # ]
    # liste_callbacks = [s for s in liste_brute if manager.regexp.match(s)]
    # print(liste_callbacks)

    print(EngineEvTypes.dict_repr)
    print('??')
    print('-'*33)
    my_li = SampleListener('tom')
    my_li.turn_on()
    print(my_li)
