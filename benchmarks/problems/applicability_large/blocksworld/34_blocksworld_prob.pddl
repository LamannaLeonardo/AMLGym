

(define (problem bw_rand_7)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 - block)
(:init
(handempty)
(on b1 b5)
(on b2 b4)
(ontable b3)
(on b4 b3)
(on b5 b2)
(ontable b6)
(on b7 b6)
(clear b1)
(clear b7)
)
(:goal
(and
(on b1 b4)
(on b2 b1)
(on b3 b5)
(on b4 b6)
(on b5 b7))
)
)


