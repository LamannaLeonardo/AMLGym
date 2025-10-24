

(define (problem bw_rand_7)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 - block)
(:init
(handempty)
(on b1 b2)
(on b2 b7)
(on b3 b4)
(ontable b4)
(ontable b5)
(ontable b6)
(on b7 b6)
(clear b1)
(clear b3)
(clear b5)
)
(:goal
(and
(on b1 b7)
(on b2 b1)
(on b3 b5)
(on b5 b6)
(on b6 b2)
(on b7 b4))
)
)


