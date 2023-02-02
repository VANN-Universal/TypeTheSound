def pretty_combination(combi):
    combi = set(combi)
    prettified_combi = []
    for key in combi:
        prettified_combi.append(
            str(key).replace("'", "").replace("Key.", "")
        )
    return " + ".join(prettified_combi)


def shorten_path(path, max_len=50):
    if len(path) > max_len:
        path = path.split("/")[-1]
    if len(path) > max_len:
        path = path[:max_len // 2 - 5] + "  ...  " + path[-max_len // 2 + 5:]
    return path
