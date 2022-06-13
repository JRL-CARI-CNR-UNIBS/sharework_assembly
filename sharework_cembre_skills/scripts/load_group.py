#!/usr/bin/env python3

import rospy

import object_loader_msgs.srv
import object_loader_msgs.msg


def main():
    rospy.init_node('load_group')

    add_group = rospy.ServiceProxy('/add_objects_group', object_loader_msgs.srv.AddObjectsGroup)
    add_group.wait_for_service()
    add_group("storages")
    add_group("P1_A1653")
    add_group("P2_A1653")

if __name__ == '__main__':
    main()
