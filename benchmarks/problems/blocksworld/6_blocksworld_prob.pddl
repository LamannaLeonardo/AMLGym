

(define (problem bw-rand-6)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 - block)
(:init
(handempty)
(on b1 b6)
(ontable b2)
(on b3 b5)
(ontable b4)
(on b5 b1)
(on b6 b2)
(clear b3)
(clear b4)
)
(:goal
(and
(on b1 b3)
(on b3 b6)
(on b4 b2)
(on b5 b4)
(on b6 b5))
)
)


