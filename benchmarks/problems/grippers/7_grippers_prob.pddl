(define (problem gripper-3-10-5)
(:domain gripper-strips)
(:objects robot1 robot2 robot3 - robot
rgripper1 lgripper1 rgripper2 lgripper2 rgripper3 lgripper3 - gripper
room1 room2 room3 room4 room5 room6 room7 room8 room9 room10 - room
ball1 ball2 ball3 ball4 ball5 - ball)
(:init
(at-robby robot1 room4)
(free robot1 rgripper1)
(free robot1 lgripper1)
(at-robby robot2 room10)
(free robot2 rgripper2)
(free robot2 lgripper2)
(at-robby robot3 room9)
(free robot3 rgripper3)
(free robot3 lgripper3)
(at ball1 room4)
(at ball2 room1)
(at ball3 room6)
(at ball4 room8)
(at ball5 room8)
)
(:goal
(and
(at ball1 room4)
(at ball2 room8)
(at ball3 room2)
(at ball4 room1)
(at ball5 room10)
)
)
)
