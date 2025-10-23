(define (problem gripper_2_8_4)
(:domain gripper_strips)
(:objects robot1 robot2 - robot
rgripper1 lgripper1 rgripper2 lgripper2 - gripper
room1 room2 room3 room4 room5 room6 room7 room8 - room
ball1 ball2 ball3 ball4 - ball)
(:init
(at_robby robot1 room4)
(free robot1 rgripper1)
(free robot1 lgripper1)
(at_robby robot2 room7)
(free robot2 rgripper2)
(free robot2 lgripper2)
(at ball1 room8)
(at ball2 room6)
(at ball3 room4)
(at ball4 room7)
)
(:goal
(and
(at ball1 room2)
(at ball2 room6)
(at ball3 room2)
(at ball4 room7)
)
)
)
