

(define (problem bw_rand_4)
(:domain blocksworld)
(:objects b1 b2 b3 b4 - block)
(:init
(handempty)
(on b1 b4)
(ontable b2)
(on b3 b2)
(on b4 b3)
(clear b1)
)
(:goal
(and
(on b2 b1)
(on b4 b3))
)
)


