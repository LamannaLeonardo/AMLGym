

(define (problem bw_rand_8)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b8)
(on b2 b5)
(ontable b3)
(on b4 b3)
(on b5 b1)
(ontable b6)
(on b7 b6)
(on b8 b7)
(clear b2)
(clear b4)
)
(:goal
(and
(on b1 b7)
(on b2 b5)
(on b4 b6)
(on b5 b4)
(on b6 b1)
(on b8 b2))
)
)


