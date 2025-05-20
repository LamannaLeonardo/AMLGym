

(define (problem bw-rand-4)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 - block)
(:init
(handempty)
(ontable b1)
(on b2 b1)
(on b3 b4)
(ontable b4)
(clear b2)
(clear b3)
)
(:goal
(and
(on b1 b2)
(on b2 b3))
)
)


