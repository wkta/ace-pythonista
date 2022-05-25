"""
event manager
"""
from abc import ABC, abstractmethod
from structures.Singleton import Singleton
from structures.CircularBuffer import CircularBuffer


# default
_buffer_size = 4096


class EngiEvent:
    """needs to be compatible with pygame events"""
    def __init__(self, evtype, **kwargs):
        self.type = evtype
        for k, v in kwargs.items():
            self.__setattr__(k, v)


class Emitter:
    _taken_ids = set()
    _free_id = -3498778*10**7
    
    def __init__(self, specific_id=None):
        # - pick the id
        cls = self.__class__
        if specific_id:
            if specific_id in cls._taken_ids:
                raise ValueError(f'cannot create Emitter with id:{specific_id} its taken!')
            self._ident = specific_id
        else:
            while cls._free_id in cls._taken_ids:
                cls._free_id += 1
            self._ident = cls._free_id
            cls._free_id += 1
        # register id
        cls._taken_ids.add(self._ident)
        
        # cache the manager
        self._event_m = EventManager.instance()

    @classmethod
    def reset_class_state(cls):
        cls._taken_ids.clear()
        cls._free_id = -3498778*10**7

    @property
    def id(self):
        return self._ident

    def pev(self, ev_type, **kwargs):
        self._event_m.post(EngiEvent(ev_type, **kwargs))


class Listener(Emitter, ABC):
    def __init__(self, specific_id=None, sticky=False):
        """
        if sticky==True, the receiver won't be removed when "EventManager.soft_reset()"s
        """
        Emitter.__init__(self, specific_id)
        self.sticky = sticky

    def turn_on(self):
        self._event_m.add_listener(self)

    def turn_off(self):
        self._event_m.remove_listener(self)

    @abstractmethod
    def proc_event(self, ev):
        raise NotImplementedError


class ListenerSet:
    def __init__(self):
        self._corresp = dict()
        self._listener_ids = list()

    def add_listener(self, cog_obj):
        key = cog_obj.id
        self._corresp[key] = cog_obj
        self._listener_ids.append(key)

    def remove_listener(self, cog_obj):
        key = cog_obj.id
        self._listener_ids.remove(key)
        del self._corresp[key]

    def hard_reset(self):
        self._corresp.clear()
        del self._listener_ids[:]

    def soft_reset(self):
        ids_to_keep = set()
        past_order = list()
        for listener_id in self._listener_ids:
            if self._corresp[listener_id].sticky:
                ids_to_keep.add(listener_id)
                past_order.append(listener_id)
        self.hard_reset()
        self._corresp.update(ids_to_keep)
        self._listener_ids.extend(past_order)

    def get_size(self):
        return len(self._corresp)

    def __getitem__(self, listener_id):
        return self._corresp[listener_id]

    def __iter__(self):
        return self._listener_ids.__iter__()


@Singleton
class EventManager:
    def __init__(self):
        self._buffer = CircularBuffer(_buffer_size)

        nothing_ev = list()
        
        def _no_extr_ev():
            nonlocal nothing_ev
            return nothing_ev
        # its like a callback, and can be hacked
        self.alien_ev_provider = _no_extr_ev
        
        self._lp = ListenerSet()
        self.add_listener = self._lp.add_listener
        self.remove_listener = self._lp.remove_listener
        self.hard_reset = self._lp.hard_reset
        self.soft_reset = self._lp.soft_reset

    def set_buffer_size(self, n):
        global _buffer_size
        _buffer_size = n
        self._buffer = CircularBuffer(n)

    @property
    def count(self):
        return self._lp.get_size()

    def post(self, evobj):
        self._buffer.enqueue(evobj)

    def update(self):
        for ae in self.alien_ev_provider():
            self._buffer.enqueue(ae)
        
        n = self._buffer.size()
        for _ in range(n):
            evobj = self._buffer.dequeue()
            
            for listener_id in self._lp:
                captures_evt = self._lp[listener_id].proc_event(evobj)
                
                if captures_evt:
                    continue


# test
if __name__ == '__main__':
    e = Emitter(2-3498778*10**7)
    f = Emitter()
    g = Emitter()
    h = Emitter()
    i = Emitter()
    print(e.id, '{}}{',f.id, g.id, h.id, i.id)

    print('-----')
    class _TotoL(Listener):
        def proc_event(self, ev):#, source):
            if ev.type == 33:
                print('hmm')
    
    listener = _TotoL()
    listener.turn_on()

    evm = EventManager.instance()
    evm.post(EngiEvent(33))
    evm.update()
