(define (problem gripper-2-7-3)
(:domain gripper-strips)
(:objects robot1 robot2 - robot
rgripper1 lgripper1 rgripper2 lgripper2 - gripper
room1 room2 room3 room4 room5 room6 room7 - room
ball1 ball2 ball3 - ball)
(:init
(at-robby robot1 room7)
(free robot1 rgripper1)
(free robot1 lgripper1)
(at-robby robot2 room3)
(free robot2 rgripper2)
(free robot2 lgripper2)
(at ball1 room6)
(at ball2 room4)
(at ball3 room2)
)
(:goal
(and
(at ball1 room7)
(at ball2 room1)
(at ball3 room7)
)
)
)
