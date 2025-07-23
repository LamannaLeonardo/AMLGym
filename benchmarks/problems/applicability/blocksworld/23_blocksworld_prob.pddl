

(define (problem bw_rand_5)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 - block)
(:init
(handempty)
(ontable b1)
(on b2 b1)
(on b3 b2)
(on b4 b3)
(on b5 b4)
(clear b5)
)
(:goal
(and
(on b2 b1)
(on b3 b5)
(on b4 b2)
(on b5 b4))
)
)


