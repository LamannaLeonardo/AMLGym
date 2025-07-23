

(define (problem bw_rand_5)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 - block)
(:init
(handempty)
(on b1 b2)
(ontable b2)
(ontable b3)
(on b4 b1)
(on b5 b3)
(clear b4)
(clear b5)
)
(:goal
(and
(on b1 b5)
(on b2 b3)
(on b3 b4))
)
)


