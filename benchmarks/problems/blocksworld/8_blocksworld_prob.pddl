

(define (problem bw-rand-7)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 - block)
(:init
(handempty)
(on b1 b5)
(on b2 b6)
(on b3 b4)
(ontable b4)
(on b5 b2)
(on b6 b3)
(on b7 b1)
(clear b7)
)
(:goal
(and
(on b1 b2)
(on b2 b4)
(on b4 b7)
(on b5 b6)
(on b6 b1))
)
)


