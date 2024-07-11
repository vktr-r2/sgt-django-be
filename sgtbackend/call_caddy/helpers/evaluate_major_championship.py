def is_major(name):
    if isinstance(name, str):
        name = name.lower()
        majors = ["masters tournament", "pga championship", "the open championship", "u.s. open"]
        return name in majors
    else:
        return False