import time


def generate_name(base, prefix="swen514-t1"):
    return f"{prefix}-{base}-{int(time.time())}"

