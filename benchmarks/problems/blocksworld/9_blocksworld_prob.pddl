

(define (problem bw-rand-7)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 - block)
(:init
(handempty)
(on b1 b7)
(on b2 b1)
(ontable b3)
(ontable b4)
(on b5 b6)
(ontable b6)
(ontable b7)
(clear b2)
(clear b3)
(clear b4)
(clear b5)
)
(:goal
(and
(on b1 b2)
(on b2 b7)
(on b4 b5)
(on b5 b1))
)
)


