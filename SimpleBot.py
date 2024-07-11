from utils.EventServer import EventServer
from utils.ConfigServer import ConfigServer
from utils.TaskServer import (
    TaskServer,
    VideoCaptureTask,
    Show_VideoCapture,
    defaultTask_simple,
)

# behaviour tree
import utils.Behavior_Tree as Behavior_Tree

import time


class SimpleBot:
    def __init__(self):

        self.Status = ConfigServer(config_path="status.json")
        self.Config = ConfigServer(config_path="config.json")

        self.EventServer = EventServer(self)
        self.TaskServer = TaskServer(self)

    def init(self):

        if self.Config.variables["bot_info"]["name"] == {}:
            self.Config.variables["bot_info"]["name"] = "SimpleBot"
        if self.Config.variables["bot_info"]["bot_version"] == {}:
            self.Config.variables["bot_info"]["bot_version"] = "1.0"
        if self.Config.variables["config"]["Camera_path"] == {}:
            self.Config.variables["config"]["Camera_path"] = "0"

    def onLoad(self):
        self.video_capture = VideoCaptureTask(
            self, int(self.Config.variables["config"]["Camera_path"])
        )
        self.TaskServer.register_task("Camera1", self.video_capture)

        self.ShowFrame_task = Show_VideoCapture(self, self.video_capture)
        self.TaskServer.register_task("ShowFrame", self.ShowFrame_task)

    def onEnable(self):
        pass


if __name__ == "__main__":

    # init() -> onLoad() -> run()
    bot = SimpleBot()
    bot.init()
    bot.onLoad()

    import time

    while True:
        time.sleep(2)
        # bot.TaskServer.run()
