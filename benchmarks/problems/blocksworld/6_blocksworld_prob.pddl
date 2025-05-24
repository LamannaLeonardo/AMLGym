

(define (problem bw_rand_6)
(:domain blocksworld_4ops)
(:objects b1 b2 b3 b4 b5 b6 - block)
(:init
(handempty)
(on b1 b6)
(ontable b2)
(ontable b3)
(on b4 b3)
(on b5 b4)
(on b6 b2)
(clear b1)
(clear b5)
)
(:goal
(and
(on b1 b4)
(on b2 b3)
(on b3 b1)
(on b5 b2))
)
)


