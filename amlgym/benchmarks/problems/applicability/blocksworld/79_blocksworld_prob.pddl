

(define (problem bw_rand_4)
(:domain blocksworld)
(:objects b1 b2 b3 b4 - block)
(:init
(handempty)
(ontable b1)
(on b2 b3)
(on b3 b1)
(on b4 b2)
(clear b4)
)
(:goal
(and
(on b2 b3)
(on b3 b4))
)
)


