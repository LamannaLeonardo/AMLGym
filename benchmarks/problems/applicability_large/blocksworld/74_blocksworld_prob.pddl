

(define (problem bw_rand_7)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 - block)
(:init
(handempty)
(ontable b1)
(ontable b2)
(ontable b3)
(on b4 b2)
(ontable b5)
(on b6 b5)
(on b7 b6)
(clear b1)
(clear b3)
(clear b4)
(clear b7)
)
(:goal
(and
(on b2 b1)
(on b3 b6)
(on b7 b4))
)
)


