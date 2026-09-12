class Station:
    def __init__(self, bss: str, ssid: (str | None), frequency: int, signal: int):
        self.bss       = bss
        self.ssid      = ssid
        self.frequency = frequency
        self.signal    = signal

    def __str__(self):
        return f"(ssid={self.ssid}, freq={self.frequency}, sig={self.signal}, bss={self.bss})"
