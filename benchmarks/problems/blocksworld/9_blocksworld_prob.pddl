

(define (problem bw-rand-7)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 - block)
(:init
(handempty)
(on b1 b5)
(on b2 b6)
(ontable b3)
(ontable b4)
(on b5 b4)
(on b6 b7)
(ontable b7)
(clear b1)
(clear b2)
(clear b3)
)
(:goal
(and
(on b2 b1)
(on b4 b2)
(on b6 b3)
(on b7 b5))
)
)


