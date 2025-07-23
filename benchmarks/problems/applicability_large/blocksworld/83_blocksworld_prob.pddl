

(define (problem bw_rand_6)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 - block)
(:init
(handempty)
(on b1 b2)
(on b2 b5)
(on b3 b1)
(on b4 b6)
(ontable b5)
(ontable b6)
(clear b3)
(clear b4)
)
(:goal
(and
(on b1 b6)
(on b2 b4)
(on b4 b3)
(on b6 b2))
)
)


