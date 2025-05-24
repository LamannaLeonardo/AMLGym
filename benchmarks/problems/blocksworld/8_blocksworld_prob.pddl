

(define (problem bw_rand_7)
(:domain blocksworld_4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 - block)
(:init
(handempty)
(ontable b1)
(on b2 b7)
(on b3 b2)
(on b4 b1)
(ontable b5)
(ontable b6)
(ontable b7)
(clear b3)
(clear b4)
(clear b5)
(clear b6)
)
(:goal
(and
(on b2 b4)
(on b3 b5)
(on b5 b1))
)
)


