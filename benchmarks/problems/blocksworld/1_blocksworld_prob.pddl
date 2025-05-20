

(define (problem bw-rand-3)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 - block)
(:init
(handempty)
(ontable b1)
(ontable b2)
(on b3 b1)
(clear b2)
(clear b3)
)
(:goal
(and
(on b2 b1)
(on b3 b2))
)
)


