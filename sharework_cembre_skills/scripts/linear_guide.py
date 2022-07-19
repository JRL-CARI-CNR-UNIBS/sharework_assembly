#!/usr/bin/env python3

import rospy
import ur_dashboard_msgs.srv
import std_srvs.srv
import configuration_msgs.srv


class LinearGuide:

    def __init__(self):

        self.go_500 = rospy.Service('/linear_guide/go', ur_dashboard_msgs.srv.Load, self.go)

        self.play  = rospy.ServiceProxy('/ur10e_hw/dashboard/play', std_srvs.srv.Trigger)
        self.stop  = rospy.ServiceProxy('/ur10e_hw/dashboard/stop', std_srvs.srv.Trigger)
        self.load  = rospy.ServiceProxy('/ur10e_hw/dashboard/load_program', ur_dashboard_msgs.srv.Load)
        self.state = rospy.ServiceProxy('/ur10e_hw/dashboard/program_state', ur_dashboard_msgs.srv.GetProgramState)
        self.play.wait_for_service()


        self.config_client = rospy.ServiceProxy('/configuration_manager/start_configuration', configuration_msgs.srv.StartConfiguration)
        rospy.logdebug("[%s] waiting for service", rospy.get_name())
        self.config_client.wait_for_service()

    def go(self,req):

        rospy.loginfo("go to watch")
        cm_req=configuration_msgs.srv.StartConfigurationRequest()
        cm_req.strictness=cm_req.BEST_EFFORT
        cm_req.start_configuration="watch"
        cm_res=self.config_client(cm_req)


        self.stop()
        program=ur_dashboard_msgs.srv.LoadRequest()
        program.filename=req.filename
        load_res=self.load(program)
        self.play()
        rospy.sleep(0.5)
        while True:
            lg_state=self.state();
            if lg_state.state.state=="STOPPED":
                break

        self.stop()
        program.filename="ros1.urp"
        self.load(program)
        self.play()
        rospy.sleep(0.5)


        cm_req.start_configuration="trajectory_tracking"
        cm_res=self.config_client(cm_req)

        res=ur_dashboard_msgs.srv.LoadResponse()
        res.success=True
        res.answer=load_res.answer
        return res


def main():
    rospy.init_node('linear_guide_server')
    lg=LinearGuide()

    rospy.spin()




if __name__ == '__main__':
    main()
