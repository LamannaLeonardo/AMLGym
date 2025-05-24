

(define (problem bw_rand_7)
(:domain blocksworld_4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 - block)
(:init
(handempty)
(ontable b1)
(ontable b2)
(on b3 b4)
(ontable b4)
(ontable b5)
(on b6 b7)
(ontable b7)
(clear b1)
(clear b2)
(clear b3)
(clear b5)
(clear b6)
)
(:goal
(and
(on b1 b6)
(on b2 b3)
(on b5 b7)
(on b6 b5)
(on b7 b4))
)
)


