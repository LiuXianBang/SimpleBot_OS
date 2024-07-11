from threading import Thread
import time
import cv2


class defaultTask:
    def __init__(self, instance):
        self.instance = instance

    def run(self):
        raise NotImplementedError("You should implement this method")


class threadingTask:
    def __init__(self, instance, daemon=True) -> None:
        self.instance = instance
        self.isrunning = False
        self.thread = None
        self.daemon = daemon

    def start(self):
        if self.isrunning:
            print("Task is already running")
        else:
            self.isrunning = True
            self.thread = Thread(target=self.run, daemon=self.daemon)
            self.thread.start()

    def stop(self):
        self.isrunning = False

    def run(self):
        raise NotImplementedError("You should implement this method")


class TaskServer:
    def __init__(self, instance):
        self.instance = instance
        self.default_tasks = []
        self.multi_threads_task = []

    def register_task(self, name, task, auto_start=True):
        if isinstance(task, defaultTask) or isinstance(task, threadingTask):
            if isinstance(task, threadingTask):
                self.multi_threads_task.append([name, task, auto_start])
                if auto_start:
                    self.multi_threads_task[-1][1].start()
            if isinstance(task, defaultTask):
                self.default_tasks.append([name, task])

            task_list = []
            for task in self.default_tasks:
                task_list.append({"name": task[0], "type": "default"})
            for task in self.multi_threads_task:
                task_list.append({"name": task[0], "type": "thread"})

            self.instance.ConfigServer.variables["status"]["register_task"] = task_list

    def run(self):
        for task in self.default_tasks:
            print("schedule [%s] Default Task" % task[0])
            self.instance.ConfigServer.variables["status"]["running_task"] = {
                "name": task[0],
                "type": "default",
                "start_time": time.time(),
            }
            task[1].run()


class defaultTask_simple(defaultTask):
    def __init__(self, instance):
        super().__init__(instance)

    def run(self):
        # time.sleep(3)
        pass


class threadTask_simple(threadingTask):
    def __init__(self, instance):
        super().__init__(instance)

    def run(self):
        while self.isrunning:
            print(self.isrunning)


class VideoCaptureTask(threadingTask):
    def __init__(self, instance, src="0"):
        super().__init__(instance)
        self.capture = cv2.VideoCapture(src)
        self.grabbed, self.frame = self.capture.read()
        self.save_frame = None

    def run(self):
        while self.isrunning:
            self.grabbed, self.frame = self.capture.read()
            if self.grabbed:
                self.save_frame = None
                self.save_frame = self.frame

        if self.isrunning == False:
            self.capture.release()

    def read(self):

        return self.grabbed, self.frame
