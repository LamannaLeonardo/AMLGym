(define (problem gripper_1_5_2)
(:domain gripper_strips)
(:objects robot1 - robot
rgripper1 lgripper1 - gripper
room1 room2 room3 room4 room5 - room
ball1 ball2 - ball)
(:init
(at_robby robot1 room4)
(free robot1 rgripper1)
(free robot1 lgripper1)
(at ball1 room5)
(at ball2 room5)
)
(:goal
(and
(at ball1 room4)
(at ball2 room1)
)
)
)
