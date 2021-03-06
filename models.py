"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    # If you make changes, be sure to update the comments in this file.
    def __init__(self, designation, name, diameter, hazardous, **info):
        """Create a new `NearEarthObject`.

        :param designation: a string representing the unique identified of the NEO
        :param name: a string representing the name of the NEO it there is one
        :param diameter: a float representing the diameter in km of the NEO if there is one
        :param hazardous: A Boolean telling if the NEO is or is not hazardous
        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        # onto attributes named `designation`, `name`, `diameter`, and `hazardous`.
        # You should coerce these values to their appropriate data type and
        # handle any edge cases, such as a empty name being represented by `None`
        # and a missing diameter being represented by `float('nan')`.
        self.designation = designation
        if name and name != '':
            self.name = name
        else:
            self.name = None

        if diameter:
            try:
                self.diameter = float(diameter)
            except ValueError:
                print("Oops!  That was no valid number.  Try again...")
        else:
            self.diameter = float('nan')

        if hazardous == 'Y':
            self.hazardous = True
        else:
            self.hazardous = False

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return self.designation  # + ' ' + self.name

    def __str__(self):
        """Return `str(self)`."""
        # The project instructions include one possibility. Peek at the __repr__
        # method for examples of advanced string formatting.
        return f"A NearEarthObject with id {self.designation} (named {self.name}, diameter: {self.diameter}," \
               f" hazardous:{self.hazardous}) "

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, "
                f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})")

    def serialize(self):
        """To serialize an object.

        :return: serialized object of NearEarth
        """
        res_dict = {
            "designation": self.designation,
            "name": self.name,
            "diameter_km": self.diameter,
            "potentially_hazardous": self.hazardous
        }
        return res_dict


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    # If you make changes, be sure to update the comments in this file.
    def __init__(self, designation, time, distance, velocity, **info):
        """Create a new `CloseApproach`.

        :param time: The date and time, in UTC, at which the NEO passes closest to Earth.
        :param distance: A float representing The nominal approach distance, in astronomical units, of the NEO to Earth at the closest point.
        :param velocity: A float representing The velocity, in kilometers per second, of the NEO relative to Earth at the closest point.
        :param neo: The NearEarthObject that is making a close approach to Earth.
        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        # onto attributes named `_designation`, `time`, `distance`, and `velocity`.
        # You should coerce these values to their appropriate data type and handle any edge cases.
        # The `cd_to_datetime` function will be useful.
        self._designation = designation
        if time:
            try:
                self.time = cd_to_datetime(time)
            except ValueError:
                print("The date and time should be in UTC")
        else:
            self.time = None
        try:
            self.distance = float(distance)
        except ValueError:
            print("Distance must be a number")

        try:
            self.velocity = float(velocity)
        except ValueError:
            print("Velocity must be a number")

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        # The project instructions include one possibility. Peek at the __repr__
        # method for examples of advanced string formatting.
        return f"On {self.time_str}, {self.neo.fullname} approaches Earth " \
               f"at a distance of {self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={self.neo!r})")

    def serialize(self):
        """To serialize an object.

        :return: serialized object of Close Approach
        """
        res_dict = {
            "datetime_utc": datetime_to_str(self.time),
            "distance_au": self.distance,
            "velocity_km_s": self.velocity
        }
        return res_dict

    @property
    def designation(self):
        """Designation.

        :return: designation
        """
        return self._designation
