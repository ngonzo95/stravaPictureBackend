import random
import string
from decimal import Decimal


def randomString(n):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))


def randomDecimal(start, end, resolution):
    """Returns a random decimal number between two integers resolution
    dictates the number of decimal places"""
    wholeNumber = random.randint(start, end)
    decimal = random.randint(0, 10**resolution)
    return Decimal(str(wholeNumber) + "." + str(decimal))


def randomCord():
    """Returns a random latlong """
    return [randomDecimal(-90, 90, 6), randomDecimal(-180, 180, 6)]


def randint(a, b):
    return random.randint(a, b)
