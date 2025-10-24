

(define (problem bw_rand_5)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 - block)
(:init
(handempty)
(ontable b1)
(on b2 b5)
(ontable b3)
(on b4 b1)
(on b5 b3)
(clear b2)
(clear b4)
)
(:goal
(and
(on b1 b4)
(on b4 b2))
)
)


