

(define (problem bw-rand-6)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 - block)
(:init
(handempty)
(ontable b1)
(on b2 b4)
(on b3 b1)
(on b4 b3)
(on b5 b2)
(ontable b6)
(clear b5)
(clear b6)
)
(:goal
(and
(on b1 b3)
(on b2 b6)
(on b3 b5)
(on b6 b4))
)
)


