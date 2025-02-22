# 在Battle类前新增日志策略类
class GlobalBattleLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.handlers = []
        return cls._instance

    def add_handler(self, handler):
        self.handlers.append(handler)

    def log(self, type: str, log: str, **kwargs):
        entry = {"type": type, "log": log, **kwargs}
        for handler in self.handlers:
            handler.handle(entry)
        return entry


# 全局单例实例
battle_logger = GlobalBattleLogger()


class JSONLogHandler:
    def __init__(self, battle_log):
        self.battle_log = battle_log

    def handle(self, entry):
        self.battle_log.append(entry)


class ConsoleLogHandler:
    def handle(self, entry):
        print(f"[{entry['type']}] {entry['log']}")

# 修改Battle类的__init__方法
