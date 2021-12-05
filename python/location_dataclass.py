from dataclasses import dataclass

from position import Position, EarthPosition


@dataclass(
  init=True,
  repr=True,
  eq=True,
  order=False,
  unsafe_hash=False,
  frozen=True, # Makes the arguments inmutable if set True. This way class will be hashable.
)
class Location:
  name: str
  position: Position

  def __post_init__(self):
	  if self.name == "":
	    raise ValueError("Location name cannot be empty")

hong_kong = Location("Hong Kong", EarthPosition(22.29, 114.16))
stockholm = Location("Stockholm", EarthPosition(59.33, 18.06))
cape_town = Location("Cape Town", EarthPosition(-33.93, 18.06))
