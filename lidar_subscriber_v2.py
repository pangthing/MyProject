from turtle import distance
import rospy
# from std_msgs.msg import PointCloud2
# from sensor_msgs.msg import _PointCloud
from sensor_msgs.msg import PointCloud
import math
import numpy as np

class PointsManager:
    def __init__(self):
        self.objects_list = []
        self.coords = []
        self.distances = []

    def checkconflict(self):
        for coord in self.coords:
            if coord>-0.3 and coord<0.3:
                return True
    
    def make_objects(self):
        count = 0
        templist = []
        endpoints_distance = get_distance(self.coords[0], self.coords[-1])
        if endpoints_distance < 0.05:
            count = -1
            templist.extend([self.coords[-1], self.coords[0]])
            while get_distance(self.coords[count], self.coords[count-1]) < 0.05:
                templist.insert(0, self.coords[count-1])
                count -= 1
            count = 0
            while get_distance(self.coords[count], self.coords[count+1]) < 0.05:

            distance = get_distance(self.coords[count], self.coords[count-1])
            if distance

def get_distance(x, y):
    return math.sqrt(x**2 + y**2)

def get_value(geometry_msg):
    distance = get_distance(geometry_msg.x**2, geometry_msg.y**2)
    angle = (math.atan2(geometry_msg.y, geometry_msg.x)) * 180 / math.pi

    return distance, angle

def control(data):
    angles_list = []
    angles_list_n = []
    angles_list_p = []
    tempangle_n = -0.1
    tempangle_p = 0.1
    turn_direction = ""
    temppoint = None
    line_points = []

    for points in data.points:
        distance, angle = get_value(points)

        if distance<0.5 and (angle>-15 and angle<15):
            angles_list.append(angle)

            if tempangle_n > angle:
                tempangle_n = angle
            elif tempangle_p < angle:
                tempangle_p = angle

            if temppoint != None:
                distance = math.sqrt((points.x-temppoint.x)**2 + (points.y-temppoint.y)**2)
                if distance < 0.1 and (points.x>-0.2 and points.x<0.2):
                    # line_points.append([points.x, points.y, temppoint.x, temppoint.y])     
                    print("Object detected!!!")

        temppoint = points

#    if len(angles_list) == 0:
#        return turn_direction
#    else:
#        print("Object detected!!!")

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

