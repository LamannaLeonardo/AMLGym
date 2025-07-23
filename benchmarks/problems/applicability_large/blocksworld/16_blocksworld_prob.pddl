

(define (problem bw_rand_9)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(on b1 b2)
(ontable b2)
(on b3 b7)
(on b4 b5)
(on b5 b8)
(on b6 b9)
(ontable b7)
(on b8 b6)
(on b9 b1)
(clear b3)
(clear b4)
)
(:goal
(and
(on b2 b1)
(on b3 b2)
(on b4 b6)
(on b5 b4)
(on b6 b8)
(on b7 b3)
(on b8 b7))
)
)


