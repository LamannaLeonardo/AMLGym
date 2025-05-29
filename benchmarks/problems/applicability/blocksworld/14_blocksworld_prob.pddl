

(define (problem bw_rand_5)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 - block)
(:init
(handempty)
(on b1 b4)
(ontable b2)
(on b3 b1)
(ontable b4)
(on b5 b2)
(clear b3)
(clear b5)
)
(:goal
(and
(on b2 b3)
(on b3 b1)
(on b4 b2)
(on b5 b4))
)
)


