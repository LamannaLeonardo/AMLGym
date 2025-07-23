

(define (problem bw_rand_7)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 - block)
(:init
(handempty)
(on b1 b2)
(ontable b2)
(ontable b3)
(on b4 b5)
(on b5 b7)
(ontable b6)
(on b7 b3)
(clear b1)
(clear b4)
(clear b6)
)
(:goal
(and
(on b1 b4)
(on b2 b1)
(on b3 b6)
(on b4 b5)
(on b5 b7)
(on b6 b2))
)
)


