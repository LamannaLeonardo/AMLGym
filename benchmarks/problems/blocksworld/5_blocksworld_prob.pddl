

(define (problem bw-rand-5)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 - block)
(:init
(handempty)
(ontable b1)
(on b2 b5)
(ontable b3)
(ontable b4)
(on b5 b1)
(clear b2)
(clear b3)
(clear b4)
)
(:goal
(and
(on b1 b4)
(on b2 b3))
)
)


