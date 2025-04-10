"""Stream package initializer."""

from tap_opentable.streams.restaurants import RestaurantsStream
from tap_opentable.streams.reservations import ReservationsStream
from tap_opentable.streams.menus import MenusStream
from tap_opentable.streams.reviews import ReviewsStream
from tap_opentable.streams.availability import AvailabilityStream

__all__ = [
    "RestaurantsStream",
    "ReservationsStream",
    "MenusStream",
    "ReviewsStream",
    "AvailabilityStream",
] 