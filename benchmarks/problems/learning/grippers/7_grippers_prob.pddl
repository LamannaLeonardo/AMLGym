(define (problem gripper_3_10_5)
(:domain gripper_strips)
(:objects robot1 robot2 robot3 - robot
rgripper1 lgripper1 rgripper2 lgripper2 rgripper3 lgripper3 - gripper
room1 room2 room3 room4 room5 room6 room7 room8 room9 room10 - room
ball1 ball2 ball3 ball4 ball5 - ball)
(:init
(at_robby robot1 room10)
(free robot1 rgripper1)
(free robot1 lgripper1)
(at_robby robot2 room10)
(free robot2 rgripper2)
(free robot2 lgripper2)
(at_robby robot3 room10)
(free robot3 rgripper3)
(free robot3 lgripper3)
(at ball1 room3)
(at ball2 room8)
(at ball3 room10)
(at ball4 room10)
(at ball5 room3)
)
(:goal
(and
(at ball1 room5)
(at ball2 room5)
(at ball3 room2)
(at ball4 room4)
(at ball5 room7)
)
)
)
