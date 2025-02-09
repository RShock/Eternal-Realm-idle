import itertools

# 实现一个单例模式装饰器
def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


id_counter = itertools.count(start=1)


class IDComponent:
    _id_counter = 0

    def __init__(self):
        IDComponent._id_counter += 1
        self._id = IDComponent._id_counter

    @property
    def id(self) -> int:
        return self._id
