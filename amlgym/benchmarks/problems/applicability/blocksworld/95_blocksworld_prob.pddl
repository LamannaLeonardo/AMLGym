

(define (problem bw_rand_5)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 - block)
(:init
(handempty)
(on b1 b4)
(on b2 b1)
(on b3 b2)
(on b4 b5)
(ontable b5)
(clear b3)
)
(:goal
(and
(on b1 b3)
(on b2 b1)
(on b4 b5)
(on b5 b2))
)
)


