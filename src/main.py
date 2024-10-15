# Importing requireed librairies
import URBasic, sys, math, os, tkinter.messagebox, platform, webbrowser, urx, numpy as np, tkinter as tk
from tkinter import ttk
from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper

# Variables that will be display in the UI
joints_name = ["Base", "Shoulder", "Elbow", "Wrist1", "Wrist2", "Wrist3"]

events = [  "Software started", #0
            "Joints moved", #1
            "TCP moved", #2
            "Get TCP", #3
            "Get Joints", #4
            "Gripper closed", #5
            "Gripper opened", #6
            "Gripper position set by user", #7
            "Theme changed", #8
            "Notice opened", #9
            "Robot at home position",] #10

# The class
class URSarii:

    # __init__ start when you call URSarii class
    def __init__(self):
        self.os_adaptation()
        self.gui()

    # Adapation for your operating system (important for the UI on windows)
    def os_adaptation(self):
        current_os = platform.system()
        if current_os == "Windows":
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1) # UI not blurred
            self.link = os.getcwd() + '\doc\doc.pdf'
        elif current_os == "Linux":
            self.link = os.getcwd() + '/doc/doc.pdf'
        elif current_os == "Darwin": #Mac detected
            tkinter.messagebox.showerror(title="Wrong Operating System", message="This software hasn't been tested on MacOS. Please use Linux or Windows.")
            sys.exit(0)
        else:
            tkinter.messagebox.showerror(title="Unknown Operating System", message="Unknown operating system. Please use Linux or Windows.")
            sys.exit(0)
        tkinter.messagebox.showinfo(title="Requirements", message=f"Detected OS : {current_os}.\n\nClick OK when you are connected on the same network as the robot and set your IP accordingly.")

    # Connection to UR_Robot
    def ur_connect(self):
        try:
            self.robotmodel = URBasic.robotModel.RobotModel()
            self.robot = URBasic.urScriptExt.UrScriptExt(host=self.ip.get(), robotModel=self.robotmodel)
            self.robot.reset_error()
            self.urxrobot = urx.Robot(self.ip.get())
            self.robotiqgrip = Robotiq_Two_Finger_Gripper(self.urxrobot)
            self.ur_home()
            self.ur_get_joints_pose()
            self.ur_get_tcp_pose()
            tkinter.messagebox.showinfo(title="Information", message=f"You are connected to the robot.")
            self.state_connect.configure(text="Robot State : Connected")
        except:
            tkinter.messagebox.showerror(title="Information", message=f"You are not connected to the robot.\nPlease check your settings.")
            self.state_connect.configure(text="Robot State : Disconnected")
            #raise Exception("Erreur connexion au robot")

    def ur_check_vel_acc(self):
        if float(self.acceleration.get()) > 0.1 or float(self.velocity.get()) > 1 :
            tkinter.messagebox.showwarning(title = "Security Alert", message = "Velocity or Acceleration is very high, it can be dangerous.")

    # Stopping UR Connecton and going back to home
    def ur_close(self):
        self.ur_home()
        self.close_robotiq_gripper()
        tkinter.messagebox.showinfo(title="Information", message=f"The sofware will close.")
        self.robot.close()
        self.urxrobot.close()
        sys.exit(0)

    # Get joints pose
    def ur_get_joints_pose(self):
        joints_pose = self.robot.get_actual_joint_positions()

        self.j1.delete(0,tk.END)
        self.j2.delete(0,tk.END)
        self.j3.delete(0,tk.END)
        self.j4.delete(0,tk.END)
        self.j5.delete(0,tk.END)
        self.j6.delete(0,tk.END)

        #print("Joints : ", joints_pose)
        self.j1.insert(0,joints_pose[0])
        self.j2.insert(0,joints_pose[1])
        self.j3.insert(0,joints_pose[2])
        self.j4.insert(0,joints_pose[3])
        self.j5.insert(0,joints_pose[4])
        self.j6.insert(0,joints_pose[5])
        self.last_activity.config(text=f"Last activity : {events[4]}")

    # Get tcp pose
    def ur_get_tcp_pose(self):
        self.tcp_pose = URBasic.UrScript.get_actual_tcp_pose(self.robot, wait = True)
        #print(self.tcp_pose)
        self.tcp1.delete(0,tk.END)
        self.tcp2.delete(0,tk.END)
        self.tcp3.delete(0,tk.END)
        self.tcp4.delete(0,tk.END)
        self.tcp5.delete(0,tk.END)
        self.tcp6.delete(0,tk.END)

        self.tcp1.insert(0,self.tcp_pose[0])
        self.tcp2.insert(0,self.tcp_pose[1])
        self.tcp3.insert(0,self.tcp_pose[2])
        self.tcp4.insert(0,self.tcp_pose[3])
        self.tcp5.insert(0,self.tcp_pose[4])
        self.tcp6.insert(0,self.tcp_pose[5])
        self.last_activity.config(text=f"Last activity : {events[3]}")

    # Go to home pose
    def ur_home(self):
        self.robot.movej(q=[0, -math.pi, math.pi/2, -math.pi/2, math.pi/2, 0], a=self.acceleration.get(), v=self.velocity.get(), t =0, r =0, wait = True, pose=None)
        self.ur_get_tcp_pose()
        self.ur_get_joints_pose()
        self.last_activity.config(text=f"Last activity : {events[10]}")

    # Move ur tcp
    def ur_move_tcp(self):
        self.ur_check_vel_acc()
        reverse_kinematics_corresponding_V2 = []
        tcp_values_float = []
        tcp_values_str = [self.tcp1.get(), self.tcp2.get(),self.tcp3.get(),self.tcp4.get(),self.tcp5.get(), self.tcp6.get()]
        for i in range(len(tcp_values_str)):
            tcp_values_float.append(np.float64(tcp_values_str[i]))
        reverse_kinematics_corresponding = URBasic.UrScript.get_inverse_kin(self.robot, x = tcp_values_float, qnear=None, maxPositionError =0.0001, maxOrientationError =0.0001)
        for i in range(len(reverse_kinematics_corresponding)):
            reverse_kinematics_corresponding_V2.append(float(reverse_kinematics_corresponding[i]))
        #print(reverse_kinematics_corresponding)

        self.robot.movej(q=reverse_kinematics_corresponding_V2, a=self.acceleration.get(), v=self.velocity.get(), t =0, r =0, wait = True, pose=None)

        # Clearing joints value from entries
        tcp_values_float.clear()
        tcp_values_str.clear()
        self.ur_get_tcp_pose()
        self.last_activity.config(text=f"Last activity : {events[2]}")

    # Move ur joint
    def ur_move_joint(self):
        self.ur_check_vel_acc()
        # Génération liste pour envoi données
        joints_values_float = []
        joints_values_str = [self.j1.get(), self.j2.get(),self.j3.get(),self.j4.get(),self.j5.get(), self.j6.get()]
        for i in range(len(joints_values_str)):
            joints_values_float.append(float(joints_values_str[i]))
        
        if self.move_type.get() == 0:
            self.robot.movej(q=joints_values_float, a=self.acceleration.get(), v=self.velocity.get(), t =0, r =0, wait = True, pose=None)
        if self.move_type.get() == 1:
            self.robot.movel(q=joints_values_float, a=self.acceleration.get(), v=self.velocity.get(), t =0, r =0, wait = True, pose=None)
        if self.move_type.get() == 2:
            self.robot.movec(q_to = joints_values_float, a=self.acceleration.get(), v=self.velocity.get(), r =0, wait = True)
        # Send pos to robot using tkinter entries
        self.ur_get_joints_pose()
        # MAJ dernière activité
        self.last_activity.config(text=f"Last activity : {events[1]}")

        # Clear joints value from entries
        joints_values_float.clear()
        joints_values_str.clear()

    # Opening the gripper between 0 and 255 int
    def int_robotiq_gripper(self):
        slider_value = int(self.grippervalue.get())
        if slider_value > 255:
            slider_value = 255
        if slider_value < 0:
            slider_value = 0
        self.tcp1.delete(0,tk.END)        
        self.tcp2.delete(0,tk.END)
        self.tcp3.delete(0,tk.END)
        self.tcp4.delete(0,tk.END)
        self.tcp5.delete(0,tk.END)
        self.tcp6.delete(0,tk.END)
        self.robotiqgrip.gripper_action(slider_value)
        self.last_activity.config(text=f"Last activity : {events[7]}")

    # Opening the gripper
    def open_robotiq_gripper(self):
        self.robotiqgrip.open_gripper()
        self.last_activity.config(text=f"Last activity : {events[6]}")

    # Closing the gripper
    def close_robotiq_gripper(self):
        self.robotiqgrip.close_gripper()
        self.last_activity.config(text=f"Last activity : {events[5]}")
    # Changing color theme
    def change_gui_theme(self):
        if self.etat_theme.get() == 0:
            self.window.tk.call("set_theme", "light")
        if self.etat_theme.get() == 1:
            self.window.tk.call("set_theme", "dark")
        self.last_activity.config(text=f"Last activity : {events[8]}")
    
    # Tkinter graphical user interface
    def gui(self):
        padding_x = 15
        padding_y = 15

        # INTERFACE tk
        self.window = tk.Tk()
        self.window.title('IUT BORDEAUX - DPT. GEII- HMI COBOT UNIVERSAL ROBOT 3')
        self.window.geometry("1700x750")

        # test theme
        self.window.tk.call("source", "azure.tcl")
        self.window.tk.call("set_theme", "light")

        ###### SECTION 1 ######
        bt_joints_values = ttk.Button(self.window, text="Get JOINTS angles", command = self.ur_get_joints_pose)
        bt_joints_values.grid(row=0, column=0, padx=padding_x, pady=padding_y)

        # Labels of joints
        ttk.Label(self.window, text=joints_name[0]).grid(row = 1, column=0, padx=padding_x, pady=padding_y)
        ttk.Label(self.window, text=joints_name[1]).grid(row = 2, column=0, padx=padding_x, pady=padding_y)
        ttk.Label(self.window, text=joints_name[2]).grid(row = 3, column=0, padx=padding_x, pady=padding_y)
        ttk.Label(self.window, text=joints_name[3]).grid(row = 4, column=0, padx=padding_x, pady=padding_y)
        ttk.Label(self.window, text=joints_name[4]).grid(row = 5, column=0, padx=padding_x, pady=padding_y)
        ttk.Label(self.window, text=joints_name[5]).grid(row = 6, column=0, padx=padding_x, pady=padding_y)

        # Entries corresponding to joints
        self.j1 = ttk.Entry(self.window)
        self.j2 = ttk.Entry(self.window)
        self.j3 = ttk.Entry(self.window)
        self.j4 = ttk.Entry(self.window)
        self.j5 = ttk.Entry(self.window)
        self.j6 = ttk.Entry(self.window)

        # Positions of entries of joints
        self.j1.grid(row = 1, column=1, padx=padding_x, pady=padding_y)
        self.j2.grid(row = 2, column=1, padx=padding_x, pady=padding_y)
        self.j3.grid(row = 3, column=1, padx=padding_x, pady=padding_y)
        self.j4.grid(row = 4, column=1, padx=padding_x, pady=padding_y)
        self.j5.grid(row = 5, column=1, padx=padding_x, pady=padding_y)
        self.j6.grid(row = 6, column=1, padx=padding_x, pady=padding_y)

        self.move_type = tk.IntVar(self.window)

        # Selection mode mouvement
        ttk.Radiobutton(self.window, text ="MoveJ", variable = self.move_type, value = 0).grid(row = 7, column=0, padx=padding_x, pady=padding_y)
        ttk.Radiobutton(self.window, text ="MoveL", variable = self.move_type, value = 1).grid(row = 8, column=0, padx=padding_x, pady=padding_y)
        ttk.Radiobutton(self.window, text ="MoveC", variable = self.move_type, value = 2).grid(row = 9, column=0, padx=padding_x, pady=padding_y)

        # btn_Move_Joints
        btn_move_joints = ttk.Button(self.window, text = "Move JOINTS",command = self.ur_move_joint)
        btn_move_joints.grid(row = 11, column=1, padx=padding_x, pady=padding_y)

        ###### SECTION 2 ######

        # IP UR3
        ttk.Label(self.window, text="Robot IP").grid(row = 0,  column=5, padx=padding_x, pady=padding_y)
        self.ip = ttk.Entry(self.window)
        self.ip.insert(0,"192.168.0.37")
        self.ip.grid(row = 0,  column=6, padx=padding_x, pady=padding_y)

        # ACCELERATION
        ttk.Label(self.window, text="Robot Acceleration (m/s2)").grid(row = 1,  column=5, padx=padding_x, pady=padding_y)
        self.acceleration = ttk.Entry(self.window)
        self.acceleration.insert(0,"0.1")
        self.acceleration.grid(row = 1,  column=6, padx=padding_x, pady=padding_y)
        # VELOCITY

        ttk.Label(self.window, text="Robot Velocity (m/s)").grid(row = 2,  column=5, padx=padding_x, pady=padding_y)
        self.velocity = ttk.Entry(self.window)
        self.velocity.insert(0,"0.1")
        self.velocity.grid(row = 2,  column=6, padx=padding_x, pady=padding_y)

        # get tcp pose
        btn_GET_TCP_POS = ttk.Button(self.window, text="CONNECT", command = self.ur_connect)
        btn_GET_TCP_POS.config()
        btn_GET_TCP_POS.grid(row = 3,  column=6, padx=padding_x, pady=padding_y)

        # Home Pos
        btn_POSE_INIT= ttk.Button(self.window, text = "HOME",command = self.ur_home)
        btn_POSE_INIT.grid(row = 0,  column=4, padx=padding_x, pady=padding_y)

        # btn_QUIT
        btn_DISCONNECT = ttk.Button(self.window, text="DISCONNECT", command = self.ur_close)
        btn_DISCONNECT.grid(row = 4,  column=6, padx=padding_x, pady=padding_y)

        ##### SECTION3 ####


        # get tcp pose
        btn_GET_TCP_POS = ttk.Button(self.window, text="Get TCP Pose", command = self.ur_get_tcp_pose)
        btn_GET_TCP_POS.grid(row = 0,  column=2, padx=padding_x, pady=padding_y)

        ttk.Label(self.window, text="X").grid(row = 1, column=2, padx=padding_x, pady=padding_y)
        ttk.Label(self.window, text="Y").grid(row = 2, column=2, padx=padding_x, pady=padding_y)
        ttk.Label(self.window, text="Z").grid(row = 3, column=2, padx=padding_x, pady=padding_y)
        ttk.Label(self.window, text="Rx").grid(row = 4, column=2, padx=padding_x, pady=padding_y)
        ttk.Label(self.window, text="Ry").grid(row = 5, column=2, padx=padding_x, pady=padding_y)
        ttk.Label(self.window, text="Rz").grid(row = 6, column=2, padx=padding_x, pady=padding_y)

        self.tcp1 = ttk.Entry(self.window)
        self.tcp2 = ttk.Entry(self.window)
        self.tcp3 = ttk.Entry(self.window)
        self.tcp4 = ttk.Entry(self.window)
        self.tcp5 = ttk.Entry(self.window)
        self.tcp6 = ttk.Entry(self.window)

        self.tcp1.grid(row = 1, column=3, padx=padding_x, pady=padding_y)
        self.tcp2.grid(row = 2, column=3, padx=padding_x, pady=padding_y)
        self.tcp3.grid(row = 3, column=3, padx=padding_x, pady=padding_y)
        self.tcp4.grid(row = 4, column=3, padx=padding_x, pady=padding_y)
        self.tcp5.grid(row = 5, column=3, padx=padding_x, pady=padding_y)
        self.tcp6.grid(row = 6, column=3, padx=padding_x, pady=padding_y)

        # TCP
        btn_SEND_TCP_POS = ttk.Button(self.window, text="Move TCP", command = self.ur_move_tcp)
        btn_SEND_TCP_POS.grid(row = 7,  column=3, padx=padding_x, pady=padding_y)

        # Label derniere activitée enregistrée
        self.last_activity = ttk.Label(self.window, text=f"Last activity : {events[0]}")
        self.last_activity.grid(row = 7,  column=6, padx=padding_x, pady=padding_y)
        
        # Gripper Open
        btn_GRIPPER_Open = ttk.Button(self.window, text="OPEN Gripper", command = self.open_robotiq_gripper)
        btn_GRIPPER_Open.grid(row = 1,  column=4, padx=padding_x, pady=padding_y)

        # Gripper Close
        btn_GRIPPER_Close = ttk.Button(self.window, text="CLOSE Gripper", command = self.close_robotiq_gripper)
        btn_GRIPPER_Close.grid(row = 2,  column=4, padx=padding_x, pady=padding_y)

        # Swicth for dark/light theme
        self.etat_theme = tk.IntVar()
        self.switch_inverse_theme = ttk.Checkbutton(self.window,style="Switch.TCheckbutton", command = self.change_gui_theme, variable=self.etat_theme, onvalue=1, offvalue=0)
        self.switch_inverse_theme.grid(row = 6,  column=6, padx=padding_x, pady=padding_y)

        # Notice
        btn_NOTICE = ttk.Button(self.window, text="Notice", command = self.notice)
        btn_NOTICE.grid(row = 5,  column=6, padx=padding_x, pady=padding_y)

        # Gripper value as int between 0 and 255
        self.grippervalue = ttk.Entry(self.window)
        self.grippervalue.grid(row = 3,  column=4, padx=padding_x, pady=padding_y)
        self.grippervalue.insert(0,"int between 0-255")
        btn_GripperCommand = ttk.Button(self.window, text="Custom Position Gripper", command = self.int_robotiq_gripper)
        btn_GripperCommand.grid(row = 4,  column=4, padx=padding_x, pady=padding_y)
        
        #State Connection
        self.state_connect = ttk.Label(self.window, text = "Robot State : Disconnected")
        self.state_connect.grid(row =8, column=6)
        
        # Credits
        creators = "Licence Pro SARII - IUT de Bordeaux- Promotion 2022-2023\nAuthors: BRUNO Paul & PELE Alexis - Alternants Siemens\nV1.0 - Glowing Turtle"
        ttk.Label(self.window, text = creators, font = 'Arial 8 italic').grid(row=9, column=6)

        # self.window stay open
        self.window.mainloop()

    # Opening the .pdf file containing the explain file
    def notice(self):
        webbrowser.open(self.link)

URSarii() # Starting the librarie