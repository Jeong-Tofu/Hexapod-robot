import math

#Hexapod_IK

#Pos x,y,z를 담기 위한 Point 클래스 생성
# class Point:
#     def __init__(self, pos_1, pos_2, pos_3):
#         self.pos_1 = pos_1
#         self.pos_2 = pos_2
#         self.pos_3 = pos_3

def inverse_kinematics(x, y, z):
    theta_1 = 0
    theta_2 = 0
    theta_3 = 0

    phi_1 = 0
    phi_2 = 0
    phi_3 = 0

    pos_1 = 0
    pos_2 = 0
    pos_3 = 0

    r_1 = z
    r_2 = math.sqrt(x**2 + y**2)
    r_3 = math.sqrt(r_1**2 + r_2**2)

    a_2 = 90  # [mm]
    a_3 = 111.878  # [mm]

    todegree = 180 / math.pi

    phi_2 = math.atan2(r_2, r_1)
    phi_1 = math.acos((a_3**2 - a_2**2 - r_3**2) / (-2 * a_2 * r_3))

    theta_2 = phi_2 - phi_1
    pos_2= theta_2 * todegree

    phi_3 = math.acos((r_3**2 - a_3**2 - a_2**2) / (-2 * a_2 * a_3))

    theta_3 = phi_3
    pos_3 = -(180 - theta_3 * todegree)

    theta_1 = math.atan2(y, x)
    pos_1 = theta_1 * todegree

    return pos_1, pos_2, pos_3
