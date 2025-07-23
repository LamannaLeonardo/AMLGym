

(define (problem bw_rand_8)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b2)
(on b2 b8)
(ontable b3)
(ontable b4)
(on b5 b6)
(on b6 b7)
(ontable b7)
(ontable b8)
(clear b1)
(clear b3)
(clear b4)
(clear b5)
)
(:goal
(and
(on b1 b5)
(on b2 b3)
(on b3 b6)
(on b5 b2)
(on b6 b4)
(on b7 b1)
(on b8 b7))
)
)


