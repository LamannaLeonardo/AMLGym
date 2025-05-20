

(define (problem bw-rand-3)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 - block)
(:init
(handempty)
(on b1 b2)
(ontable b2)
(ontable b3)
(clear b1)
(clear b3)
)
(:goal
(and
(on b1 b3))
)
)


