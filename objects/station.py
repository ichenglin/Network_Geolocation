from objects.serializable import Serializable, SerializableContent


class Station(Serializable):
    def __init__(self, bss: str, ssid: (str | None), channel: int, signal: int, all: (dict | None) = None):
        self.bss       = bss
        self.ssid      = ssid
        self.channel   = channel
        self.signal    = signal
        self.all       = all

    @classmethod
    def __import__(cls, content: SerializableContent):
        return cls(
            content.get("bss",     None),
            content.get("ssid",    None),
            content.get("channel", None),
            content.get("signal",  None),
            content.get("all",     None)
        )

    def __export__(self) -> SerializableContent:
        return {
            "bss":     self.bss,
            "ssid":    self.ssid,
            "channel": self.channel,
            "signal":  self.signal,
            "all":     self.all
        }

    def __str__(self) -> str:
        return f"(ssid={self.ssid}, chnl={self.channel}, sig={self.signal}, bss={self.bss})"

    def __repr__(self) -> str:
        return self.__str__()