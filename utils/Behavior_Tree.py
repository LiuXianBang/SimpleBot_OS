import time
from threading import Thread


class Node:
    def __init__(self):
        self.children = []

    def run(self):
        raise NotImplementedError("You should implement this method")


class Sequence(Node):
    def run(self):
        for child in self.children:
            if not child.run():
                return False
        return True


class FallBack(Node):
    def run(self):
        for child in self.children:
            if child.run():
                return True
        return False


class Action(Node):
    def __init__(self, action):
        super().__init__()
        self.action = action

    def run(self):
        return self.action()


class Condition(Node):
    def __init__(self, condition):
        super().__init__()
        self.condition = condition

    def run(self):
        return self.condition()


class Inverter(Node):
    def __init__(self, child):
        super().__init__()
        self.children = child

    def run(self):
        return not self.children.run()


class life_cycle:
    def __init__(self, handle):
        self.tick = 0
        self.frequent = 10  # hz
        self.delay = float(1 / self.frequent)
        self.max_count_tick = 100000
        self.is_running = False
        self.handle = handle

    def start(self):
        self.is_running = True
        Thread(target=self.loop, args=(), daemon=True).start()

    def loop(self):
        while self.is_running:
            time.sleep(self.delay)
            self.tick += 1
            self.handle(self.tick)
            if self.tick > self.max_count_tick:
                self.tick = 0

    def stop(self):
        self.is_running = False
