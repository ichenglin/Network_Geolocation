class Station:
    def __init__(self, bss: str, ssid: (str | None), channel: int, signal: int):
        self.bss       = bss
        self.ssid      = ssid
        self.channel   = channel
        self.signal    = signal

    def __str__(self):
        return f"(ssid={self.ssid}, chnl={self.channel}, sig={self.signal}, bss={self.bss})"

    def __repr__(self):
        return self.__str__()