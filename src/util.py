def clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)


def remap(x, from_min, from_max, to_min, to_max):
    # range check
    if from_min == from_max:
        return None

    if to_min == to_max:
        return None

    # check reversed input range
    reverse_input = False
    old_min = min(from_min, from_max)
    old_max = max(from_min, from_max)
    if not old_min == from_min:
        reverse_input = True

    # check reversed output range
    reverse_output = False
    new_min = min(to_min, to_max)
    new_max = max(to_min, to_max)
    if not new_min == to_min:
        reverse_output = True

    portion = (x - old_min) * (new_max - new_min) / (old_max - old_min)
    if reverse_input:
        portion = (old_max - x) * (new_max - new_min) / (old_max - old_min)

    result = portion + new_min
    if reverse_output:
        result = new_max - portion

    return result
