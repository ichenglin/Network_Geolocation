from objects.coordinate import Coordinate, ProximateCoordinate
from objects.station import Station


def report_samples(samples: list[Station], key: str = "signal", reverse: bool = True) -> None:
    ordered = sorted(samples, key=(lambda sample: getattr(sample, key)), reverse=reverse)
    print("\n".join(["".join([
        f"{(index + 1):<2}",
        f" | {(sample.ssid or ""):<16}"[:(16 + 3)],
        f" | Channel {sample.channel:<3}",
        f" | {sample.signal:<3} dBm",
        f" | {sample.bss}"
    ]) for index, sample in enumerate(ordered)]))

def report_distance(actual: Coordinate, guess: ProximateCoordinate, distance: int) -> None:
    print("".join([
        f"Guess:    {guess.latitude:<9}"   [:(9 + 10)],
        f", {guess.longitude:<9}"          [:(9 + 3)],
        f"\nActual:   {actual.latitude:<9}"[:(9 + 11)],
        f", {actual.longitude:<9}"         [:(9 + 3)],
        f"\nDistance: {int(distance)} meter(s)"
    ]))

def report_border() -> None:
    print("=" * 65)