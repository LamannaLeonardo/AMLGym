

(define (problem bw_rand_10)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b4)
(on b2 b1)
(ontable b3)
(on b4 b5)
(on b5 b7)
(on b6 b3)
(on b7 b10)
(ontable b8)
(on b9 b2)
(on b10 b8)
(clear b6)
(clear b9)
)
(:goal
(and
(on b2 b9)
(on b3 b6)
(on b5 b4)
(on b6 b1)
(on b8 b2)
(on b10 b5))
)
)


