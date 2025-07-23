

(define (problem bw_rand_5)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 - block)
(:init
(handempty)
(ontable b1)
(on b2 b1)
(ontable b3)
(ontable b4)
(on b5 b4)
(clear b2)
(clear b3)
(clear b5)
)
(:goal
(and
(on b4 b5)
(on b5 b1))
)
)


