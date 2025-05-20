

(define (problem bw-rand-5)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 - block)
(:init
(handempty)
(ontable b1)
(ontable b2)
(on b3 b1)
(on b4 b5)
(on b5 b2)
(clear b3)
(clear b4)
)
(:goal
(and
(on b1 b5)
(on b2 b4)
(on b3 b1)
(on b5 b2))
)
)


