(define (problem gripper_1_3_1)
(:domain gripper_strips)
(:objects robot1 - robot
rgripper1 lgripper1 - gripper
room1 room2 room3 - room
ball1 - ball)
(:init
(at_robby robot1 room2)
(free robot1 rgripper1)
(free robot1 lgripper1)
(at ball1 room2)
)
(:goal
(and
(at ball1 room3)
)
)
)
