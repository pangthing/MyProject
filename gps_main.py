from gps import *
from gps_direction import *
from naver_api import *

user_gps = [37.2486435, 127.0750234]
user_gps_str = ('127.0750234', '37.2486435')

gps_port = "/dev/ttyS0"
serial = port_setup(gps_port)

print("Start GPS coordinate Streaming ..")
count = 0

while True:
    try:
        drone_coords = parseGPSdata(serial)
        if drone_coords is not None:
            error = get_error(get_differ(drone_coords, user_gps))
            drone_coords_str = (str(drone_coords[1]), str(drone_coords[0]))
            results = get_optimal_route(drone_coords_str, user_gps_str, option='')
#            print(results)
            paths = results['route']['traoptimal'][0]['path']
#            print(drone_coords)
#            print(drone_coords_str)
#            print(user_gps)
            print(error)
            print(paths)
            break
        else:
            continue

    except Exception as e:
        print(count, e)
        count += 1
        if e == 'route':
            print(drone_coodrs)


