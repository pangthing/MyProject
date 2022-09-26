### 1. GPS <-> distance 변환 알고리즘

# GPGGA 값으로 받는다고 가정

import math

def GPGGA_to_DMS(GPGGA):
    demical, integer = math.modf(GPGGA)

    degree, minute = divmod(integer, 100)
    second = demical * 60

    return degree, minute, second

def GPS_to_DMS(GPS):
    demical, degree = math.modf(GPS)

    ms = demical * 60

    demical, minute = math.modf(ms)

    second = demical * 60

    return degree, minute, second

def get_differ(Droneloc, Goalloc):
    DroneDMS_lat = GPGGA_to_DMS(Droneloc[0])
    DroneDMS_long = GPGGA_to_DMS(Droneloc[1])
    GoalDMS_lat = GPS_to_DMS(Goalloc[0])
    GoalDMS_long = GPS_to_DMS(Goalloc[1])

    differ_lat = (DroneDMS_lat[0] - GoalDMS_lat[0], DroneDMS_lat[1] - GoalDMS_lat[1], DroneDMS_lat[2] - GoalDMS_lat[2])
    differ_long = (DroneDMS_long[0] - GoalDMS_long[0], DroneDMS_long[1] - GoalDMS_long[1], DroneDMS_long[2] - GoalDMS_long[2])

    return differ_lat, differ_long

def get_error(differ):
    North, East = differ
    N_distance = North[0]*111195 + North[1]*1853 + North[2]*30.887
    E_distance = East[0]*88804 + East[1]*1480 + East[2]*24.668

    return N_distance, E_distance

if __name__ == "__main__":
    print(GPGGA_to_DMS(3714.38712))
    print(GPS_to_DMS(37.566381))

    Drone = (3714.38712, 12704.98925)
    User = (37.566381, 126.977717)
    print(get_differ(Drone, User))

    print(get_error(get_differ(Drone, User)))
