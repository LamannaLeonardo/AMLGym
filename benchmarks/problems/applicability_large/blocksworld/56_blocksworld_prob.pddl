

(define (problem bw_rand_9)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(on b1 b4)
(ontable b2)
(on b3 b9)
(on b4 b8)
(ontable b5)
(on b6 b5)
(ontable b7)
(on b8 b2)
(on b9 b7)
(clear b1)
(clear b3)
(clear b6)
)
(:goal
(and
(on b2 b3)
(on b3 b1)
(on b5 b8)
(on b6 b2)
(on b7 b6)
(on b8 b7))
)
)


