

(define (problem bw_rand_6)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 - block)
(:init
(handempty)
(on b1 b2)
(on b2 b3)
(ontable b3)
(on b4 b6)
(on b5 b4)
(on b6 b1)
(clear b5)
)
(:goal
(and
(on b1 b6)
(on b3 b4)
(on b4 b1)
(on b5 b2)
(on b6 b5))
)
)


