

(define (problem bw_rand_8)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b7)
(on b2 b3)
(ontable b3)
(on b4 b6)
(on b5 b4)
(ontable b6)
(on b7 b2)
(on b8 b1)
(clear b5)
(clear b8)
)
(:goal
(and
(on b2 b6)
(on b3 b2)
(on b4 b7)
(on b8 b4))
)
)


