class event:
    def __init__(self,name) -> None:
        self.name = name
    def trigger(self) -> bool:
        raise NotImplementedError("You should implement this method")

class EventServer:
    def __init__(self,instance):
        self.instance = instance
        self.events_list = []
        
    def register_event(self,_event):
        if isinstance(_event, event):
            self.events_list.append(_event)
            for _event in self.events_list:
                self.instance.ConfigServer.variables["status"]["register_event"] = {"name":_event.name}

    def trigger(self,name):
        for event in self.events_list:
            if event.name == name:
                return event.trigger()
