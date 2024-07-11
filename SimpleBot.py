from utils.EventServer import *
from utils.ConfigServer import *
from utils.TaskServer import *

# behaviour tree
from utils.Behavior_Tree import *

import time


class SimpleBot:
    def __init__(self):

        self.ConfigServer = ConfigServer(config_path="config.json")
        self.ConfigServer.variables["bot_info"]["name"] = "SimpleBot"
        self.ConfigServer.variables["bot_info"]["bot_version"] = "1.0"

        self.EventServer = EventServer(self)
        self.TaskServer = TaskServer(self)

        self.video_capture = VideoCaptureTask(self, 0)
        self.TaskServer.register_task("Camera1", self.video_capture)

        defaultTask_simple1 = defaultTask_simple(self)
        defaultTask_simple2 = defaultTask_simple(self)
        self.TaskServer.register_task("default_task1", defaultTask_simple1)
        self.TaskServer.register_task("default_task2", defaultTask_simple2)


class CameraEvent(event):
    def __init__(self, name) -> None:
        super().__init__(name)

    def trigger(self) -> bool:
        return True


if __name__ == "__main__":

    bot = SimpleBot()
    CameraEvent1 = CameraEvent("Camera1")
    bot.EventServer.register_event(CameraEvent1)

    import time

    while True:
        # time.sleep(2)
        bot.TaskServer.run()

        grabbed, frame = bot.video_capture.read()
        if not grabbed:
            break
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
