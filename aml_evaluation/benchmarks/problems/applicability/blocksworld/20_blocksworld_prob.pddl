

(define (problem bw_rand_5)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 - block)
(:init
(handempty)
(ontable b1)
(ontable b2)
(on b3 b2)
(on b4 b5)
(on b5 b1)
(clear b3)
(clear b4)
)
(:goal
(and
(on b2 b4)
(on b5 b1))
)
)


