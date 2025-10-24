

(define (problem bw_rand_5)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 - block)
(:init
(handempty)
(ontable b1)
(on b2 b4)
(on b3 b2)
(on b4 b5)
(ontable b5)
(clear b1)
(clear b3)
)
(:goal
(and
(on b1 b2)
(on b3 b4)
(on b5 b1))
)
)


