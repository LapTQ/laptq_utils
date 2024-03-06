import yaml


def load_config(
        **kwargs
):
    config_path = kwargs['config_path']

    with open(config_path, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config


def update_config(
        **kwargs
):
    """Update the base config with the new config. 
    The new config must:
        * be of the same depth as the base config.
        * does not contain any key that is not in the base config if non_exist_ok is False.
    Note: Does not handle the case a value in the sub-dict is a list of dict.
    """
    base = kwargs['base']
    new = kwargs['new']
    non_exist_ok = kwargs['non_exist_ok']

    assert isinstance(base, dict) == isinstance(new, dict)
    if not isinstance(base, dict):
        return new

    for k, v_new in new.items():
        if k in base:
            v_base = base[k]                
            sub = update_config(
                base=v_base,
                new=v_new,
                non_exist_ok=non_exist_ok
            )
            base[k] = sub
        elif non_exist_ok:
            base[k] = v_new
        else:
            raise ValueError('Key {} for found in the base config while non_exist_ok is {}'.format(
                k,
                non_exist_ok
            ))
    return base