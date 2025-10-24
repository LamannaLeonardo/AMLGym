(define (problem gripper_3_9_4)
(:domain gripper_strips)
(:objects robot1 robot2 robot3 - robot
rgripper1 lgripper1 rgripper2 lgripper2 rgripper3 lgripper3 - gripper
room1 room2 room3 room4 room5 room6 room7 room8 room9 - room
ball1 ball2 ball3 ball4 - ball)
(:init
(at_robby robot1 room7)
(free robot1 rgripper1)
(free robot1 lgripper1)
(at_robby robot2 room4)
(free robot2 rgripper2)
(free robot2 lgripper2)
(at_robby robot3 room8)
(free robot3 rgripper3)
(free robot3 lgripper3)
(at ball1 room3)
(at ball2 room9)
(at ball3 room1)
(at ball4 room7)
)
(:goal
(and
(at ball1 room6)
(at ball2 room4)
(at ball3 room4)
(at ball4 room9)
)
)
)
