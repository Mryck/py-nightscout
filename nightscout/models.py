"""Models."""
import attr


@attr.s(auto_attribs=True, frozen=True)
class GlucoseMonitor:

    sgv: int
    direction: str
    date: int

    @staticmethod
    def from_dict(data: dict):
        """Return glucose data object from Nightscout API response."""
        data = data[0]
        return GlucoseMonitor(
            sgv=data.get("sgv", 0),
            direction=data.get("direction", ""),
            date=data.get("date", 0),
        )
