

(define (problem bw_rand_4)
(:domain blocksworld)
(:objects b1 b2 b3 b4 - block)
(:init
(handempty)
(on b1 b3)
(on b2 b1)
(ontable b3)
(ontable b4)
(clear b2)
(clear b4)
)
(:goal
(and
(on b3 b4)
(on b4 b1))
)
)


