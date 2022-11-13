# pygame.USEREVENT

FIRST_ENGIN_TYPE = pygame.USEREVENT



def camel_case_format(string_ac_underscores):
    words = [word.capitalize() for word in string_ac_underscores.split('_')]
    return "".join(words)


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

# first_custo_type = FIRST_ENGIN_TYPE + EngineEvTypes.size


def enum_ev_types(*sequential, **named):  # Custom events /!\ not engine events
    global first_custo_type
    # this function should be used by the custom game
    return enum_builder_generic(False, first_custo_type, *sequential, **named)
