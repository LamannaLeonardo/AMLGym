

(define (problem bw_rand_8)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(ontable b1)
(on b2 b5)
(on b3 b7)
(on b4 b8)
(ontable b5)
(on b6 b3)
(on b7 b4)
(on b8 b1)
(clear b2)
(clear b6)
)
(:goal
(and
(on b1 b8)
(on b2 b5)
(on b3 b4)
(on b4 b6)
(on b7 b2)
(on b8 b3))
)
)


