from objects.serializable import Serializable, SerializableContent


class Station(Serializable):
    def __init__(self, bss: str, ssid: (str | None), band: int, channel: int, signal: int, raw: list[str]):
        self.bss     = bss
        self.ssid    = ssid
        self.band    = band
        self.channel = channel
        self.signal  = signal
        self.raw     = raw

    @classmethod
    def __import__(cls, content: SerializableContent):
        return cls(
            content.get("bss",     None),
            content.get("ssid",    None),
            content.get("band",    None),
            content.get("channel", None),
            content.get("signal",  None),
            content.get("raw",     None)
        )

    def __export__(self) -> SerializableContent:
        return {
            "bss":     self.bss,
            "ssid":    self.ssid,
            "band":    self.band,
            "channel": self.channel,
            "signal":  self.signal,
            "raw":     self.raw
        }

    def __str__(self) -> str:
        return f"(ssid={self.ssid}, band={self.band}, chnl={self.channel}, sig={self.signal}, bss={self.bss})"

    def __repr__(self) -> str:
        return self.__str__()