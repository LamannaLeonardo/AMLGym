

(define (problem bw_rand_4)
(:domain blocksworld)
(:objects b1 b2 b3 b4 - block)
(:init
(handempty)
(ontable b1)
(on b2 b1)
(on b3 b2)
(ontable b4)
(clear b3)
(clear b4)
)
(:goal
(and
(on b3 b2)
(on b4 b3))
)
)


