# behaviour tree
import random
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


class SimpleBot:
    def __init__(self):
        self.bot_name = "SimpleBot"
        self.EventServer = EventServer()
        
        self.TaskServer = TaskServer()
        
        # defaultTask_simple1 = defaultTask_simple(self)
        # defaultTask_simple2 = defaultTask_simple(self)
        # threadTask_simple1 = threadTask_simple(self)
        # self.TaskServer.register_task("thread_task", threadTask_simple1,task_type="thread")
        # self.TaskServer.register_task("default_task", defaultTask_simple1)
        # self.TaskServer.register_task("default_task", defaultTask_simple2) 


class EventServer:
    def __init__(self):
        pass


class defaultTask:
    def __init__(self, instance):
        self.instance = instance
        
    def run(self):
        raise NotImplementedError("You should implement this method")

class threadingTask:
    def __init__(self,instance,daemon=True) -> None:
        self.instance = instance
        self.isrunning = False
        self.thread = None
        self.daemon = daemon
    
    def start(self):
        if self.isrunning:
            print("Task is already running")
        else:
            self.isrunning = True
            self.thread = Thread(target=self.run,daemon=self.daemon)
            self.thread.start()
            
    def stop(self):
        self.isrunning = False
    
    def run(self):
        raise NotImplementedError("You should implement this method")
    

class TaskServer:
    def __init__(self):
        self.default_tasks = []
        self.multi_threads_task = []

    def register_task(self, name, task,task_type="default",auto_start=True):
        if task_type == "thread":
            self.multi_threads_task.append([name, task,auto_start])
            if auto_start:
                self.multi_threads_task[-1][1].start()

        else:
            self.default_tasks.append([name, task])
            

    def run(self):
        for task in self.default_tasks:
            print("schedule [%s] Default Task" % task[0])
            task[1].run()


class defaultTask_simple(defaultTask):
    def __init__(self, instance):
        super().__init__(instance)

    def run(self):
        return

class threadTask_simple(threadingTask):
    def __init__(self, instance):
        super().__init__(instance)

    def run(self):
        while self.isrunning:
            time.sleep(1)
            print(self.isrunning)
        return

if __name__ == "__main__":

    bot = SimpleBot()
    bot.TaskServer.run()
    
    threadTask_simple1 = threadTask_simple(bot)
    bot.TaskServer.register_task("threadTask_simple", threadTask_simple1,task_type="thread") 
    
    i = 1
    while True:
        time.sleep(5)
        for task in bot.TaskServer.multi_threads_task:
            if task[0] == "threadTask_simple":
                task[1].stop()
        # i+=1
        # time.sleep(1)
        # defaultTask_simple1 = defaultTask_simple(bot)
        # bot.TaskServer.register_task("default_task%s"%i, defaultTask_simple1) 
        # bot.TaskServer.run()
