

(define (problem bw-rand-7)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 - block)
(:init
(handempty)
(ontable b1)
(ontable b2)
(on b3 b4)
(on b4 b2)
(ontable b5)
(ontable b6)
(on b7 b3)
(clear b1)
(clear b5)
(clear b6)
(clear b7)
)
(:goal
(and
(on b2 b5)
(on b3 b6)
(on b4 b1)
(on b5 b7)
(on b6 b4))
)
)


