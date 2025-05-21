

(define (problem bw-rand-4)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 - block)
(:init
(handempty)
(on b1 b2)
(on b2 b3)
(ontable b3)
(ontable b4)
(clear b1)
(clear b4)
)
(:goal
(and
(on b2 b1)
(on b4 b2))
)
)


