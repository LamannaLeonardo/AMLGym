

(define (problem bw_rand_7)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 - block)
(:init
(handempty)
(ontable b1)
(on b2 b4)
(on b3 b7)
(on b4 b6)
(on b5 b1)
(ontable b6)
(on b7 b2)
(clear b3)
(clear b5)
)
(:goal
(and
(on b2 b5)
(on b3 b6)
(on b5 b7)
(on b6 b2)
(on b7 b1))
)
)


