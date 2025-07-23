

(define (problem bw_rand_8)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b4)
(ontable b2)
(on b3 b6)
(ontable b4)
(on b5 b8)
(ontable b6)
(ontable b7)
(on b8 b3)
(clear b1)
(clear b2)
(clear b5)
(clear b7)
)
(:goal
(and
(on b1 b4)
(on b2 b3)
(on b3 b1)
(on b4 b6)
(on b6 b7)
(on b7 b5)
(on b8 b2))
)
)


