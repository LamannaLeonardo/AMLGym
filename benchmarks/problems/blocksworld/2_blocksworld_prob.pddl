

(define (problem bw-rand-4)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 - block)
(:init
(handempty)
(on b1 b2)
(on b2 b3)
(ontable b3)
(on b4 b1)
(clear b4)
)
(:goal
(and
(on b1 b3)
(on b4 b2))
)
)


