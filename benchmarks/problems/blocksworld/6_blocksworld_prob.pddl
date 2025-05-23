

(define (problem bw-rand-6)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 - block)
(:init
(handempty)
(on b1 b3)
(on b2 b6)
(on b3 b2)
(on b4 b5)
(ontable b5)
(ontable b6)
(clear b1)
(clear b4)
)
(:goal
(and
(on b1 b3)
(on b4 b1)
(on b5 b2)
(on b6 b4))
)
)


