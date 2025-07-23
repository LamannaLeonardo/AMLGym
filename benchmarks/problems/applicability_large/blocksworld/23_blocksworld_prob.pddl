

(define (problem bw_rand_6)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 - block)
(:init
(handempty)
(on b1 b4)
(on b2 b1)
(ontable b3)
(on b4 b5)
(on b5 b3)
(on b6 b2)
(clear b6)
)
(:goal
(and
(on b1 b3)
(on b3 b6)
(on b5 b4)
(on b6 b2))
)
)


