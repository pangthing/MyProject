from turtle import distance
import rospy
# from std_msgs.msg import PointCloud2
# from sensor_msgs.msg import _PointCloud
from sensor_msgs.msg import PointCloud
import math

def get_value(geometry_msg):
    distance = math.sqrt(geometry_msg.x**2 + geometry_msg.y**2)
    angle = (math.atan2(geometry_msg.y, geometry_msg.x)) * 180 / math.pi

    return distance, angle

def control(data):
    angles_list = []
    # angles_list_p = []
    tempangle_n = -0.1
    tempangle_p = 0.1
    turn_direction = ""
    point_p = None
    point_n = None


    for points in data.points:
        distance, angle = get_value(points)

        if distance<0.5 and (angle>-15 and angle<15):
            angles_list.append(angle)

            if tempangle_n > angle:
                tempangle_n = angle
                point_n = points
            elif tempangle_p < angle:
                tempangle_p = angle
                point_p = points

    if len(angles_list) == 0:
        return turn_direction
    else:
        print("Object detected!!!")
        if point_p is not None:
            print("p", point_p.x, point_p.y, tempangle_p)
        if point_n is not None:
            print("n", point_n.x, point_n.y, tempangle_n)

    if abs(tempangle_p) >= abs(tempangle_n):
        turn_direction = "right"
    else:
        turn_direction = "left"

    return turn_direction

def callback(data):
    size = len(data.points)

    if control(data) == "right":
        print("turn right!")
    elif control(data) == "left":
        print("turn left!")

def listener():
    rospy.init_node('lidar_sub', anonymous=True)
    rospy.Subscriber('point_cloud', PointCloud, callback)

    rospy.spin()

if __name__ == '__main__':
    listener()

