

(define (problem bw-rand-6)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 - block)
(:init
(handempty)
(on b1 b5)
(ontable b2)
(ontable b3)
(on b4 b3)
(on b5 b6)
(ontable b6)
(clear b1)
(clear b2)
(clear b4)
)
(:goal
(and
(on b2 b1)
(on b4 b6)
(on b5 b3)
(on b6 b2))
)
)


