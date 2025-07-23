

(define (problem bw_rand_9)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(on b1 b3)
(ontable b2)
(on b3 b9)
(on b4 b6)
(on b5 b8)
(on b6 b1)
(ontable b7)
(on b8 b2)
(on b9 b5)
(clear b4)
(clear b7)
)
(:goal
(and
(on b2 b9)
(on b5 b6)
(on b6 b4)
(on b7 b2)
(on b8 b5)
(on b9 b1))
)
)


