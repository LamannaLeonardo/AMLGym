

(define (problem bw_rand_4)
(:domain blocksworld)
(:objects b1 b2 b3 b4 - block)
(:init
(handempty)
(on b1 b3)
(on b2 b1)
(on b3 b4)
(ontable b4)
(clear b2)
)
(:goal
(and
(on b1 b4)
(on b2 b1)
(on b3 b2))
)
)


