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

from ken_enum import PseudoEnum, underscore_format, camel_case_format


# _enum_engine_ev_types(

EngineEvTypes = PseudoEnum([
    'Update',
    'Paint',

    'Gamestart',
    'Gameover',
    # (used in RPGs like niobepolis, conv<- conversation)
    'ConvStart',  #  ontains convo_obj, portrait
    'ConvFinish',
    'ConvStep',  # contains value

    'StateChange',  # contains code state_ident
    'StatePush',  # contains code state_ident
    'StatePop',

    'NetwSend',  # [num] un N°identification & [msg] un string (Async network comms)
    'NetwReceive'  # [num] un N°identification & [msg] un string (Async network comms)
], pygame.USEREVENT)


def mk_enum_game_events(x_iterable):
    return PseudoEnum(x_iterable, EngineEvTypes.first+EngineEvTypes.size)


@Singleton
class EventManager:
    def __init__(self):
        self._etype_to_listenerli = dict()
        self._cbuffer = CircularBuffer()
        self._known_ev_types = dict()  # corresp nom evenement <-> identifiant numérique
        self.regexp = None
        self.debug_mode = False

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
        # debug: print the updated regexp
        # -
        # print(regexp_prefix + rxp_body + regexp_sufix)
        self.regexp = re.compile(regexp_prefix + rxp_body + regexp_sufix)

    def subscribe(self, ename, listener_obj):
        cod = self._known_ev_types[ename]
        if cod not in self._etype_to_listenerli:
            self._etype_to_listenerli[cod] = list()
        
        self._etype_to_listenerli[cod].append(listener_obj)
        if self.debug_mode:
            print('  debug SUBSCRIBE - - - {} - {}'.format(ename, listener_obj))

    def unsubscribe(self, ename, listener_obj):
        cod = self._known_ev_types[ename]
        # if cod in self._etype_to_listenerli:
        try:
            self._etype_to_listenerli[cod].remove(listener_obj)
        except (KeyError, ValueError):
            print('***EventManager warning. Trying to remove listener_obj {}, not found!'.format(
                listener_obj.id
            ))
        if self.debug_mode:
            print('  debug UNSUBSCRIBE - - - {} - {}'.format(ename, listener_obj))
            

    def event_types_inform(self, given_extra_penum=None):
        names = list()
        self._known_ev_types = EngineEvTypes.content.copy()

        for evname,eid in EngineEvTypes.content.items():
            names.append(underscore_format(evname))

        if given_extra_penum:
            self._known_ev_types.update(given_extra_penum.content)
            for evname,eid in given_extra_penum.content.items():
                    names.append(underscore_format(evname))

        # force a {refresh regexp} op!
        self._refresh_regexp(names)


class KengiListenerObj:
    _free_listener_id = 34822

    def __init__(self):
        self._lid = self.__class__._free_listener_id
        self.__class__._free_listener_id += 1

        self._ev_manager_ref = None

        self._is_active = False
        self._inspection_res = set()
        self._tracked_ev = list()

    @property
    def id(self):
        return self._lid

    def turn_on(self):
        if self._ev_manager_ref is None:
            self._ev_manager_ref = EventManager.instance()

        # introspection & detection des on_*
        # où * représente tout type d'évènement connu du moteur, que ce soit un event engine ou un event custom ajouté
        every_method = [method_name for method_name in dir(self) if callable(getattr(self, method_name))]
        callbacks_only = [mname for mname in every_method if self._ev_manager_ref.regexp.match(mname)]

        for cbname in callbacks_only:
            # remove 'on_' prefix and convert Back to CamlCase
            self._tracked_ev.append(camel_case_format(cbname[3:]))

        # enregistrement de son activité d'écoute auprès du evt manager
        for evname in self._tracked_ev :
            self._ev_manager_ref.subscribe(evname, self)

    def turn_off(self):
        # opération contraire
        for evname in self._tracked_ev:
            self._ev_manager_ref.unsubscribe(evname, self)
        del self._tracked_ev[:]


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

    def on_player_death(self, ev):
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
    MyEvents = mk_enum_game_events(['PlayerMovement', 'PlayerDeath'])

    manager = EventManager.instance()
    # manager.debug_mode = True
    manager.event_types_inform(
        MyEvents
    )  # manager becomes self-aware of engine event types PLUS specific game ev.

    # test: disp codes
    print('~~ codes ~~')
    print(EngineEvTypes.Update)
    print(EngineEvTypes.Paint)
    print('...')
    print(EngineEvTypes.NetwReceive)
    print('and the extra:')
    print(MyEvents.PlayerMovement)
    print(MyEvents.PlayerDeath)
    print('-'*48)
    
    # test: post 5 events and updates the ev manager...
    print('method .POST called x5')
    manager.post(17, serveur='api.gaudia-tech.com', machin='ouais')
    manager.post(3, jojo='trois', nom='tom')
    manager.post(551, hp='128', nom='roger')
    manager.post(17, hp='11', nom='jojo')
    manager.post(332, hp='59878', nom='poisson')

    print('the NEW queue size=', manager._cbuffer.size())
    manager.update()
    print('after .UPDATE call, the queue size=', manager._cbuffer.size())
    print('-'*48)

    print('show me the regexp in EventManager inst?')
    print(manager.regexp)
    print('-'*48)

    print("turn on/turn off the listener..")
##    print(EngineEvTypes.content)
##    print('??')
##    print('-'*33)
    my_li = SampleListener('thomas')
    my_li.turn_on()
    my_li.turn_off()
##    print(my_li)

    # ---sandbox testing---
    enum_example = PseudoEnum(['KeyUp', 'KeyDown', 'Update' ])
