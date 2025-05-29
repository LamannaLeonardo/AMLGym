

(define (problem bw_rand_10)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b5)
(on b2 b3)
(on b3 b6)
(on b4 b10)
(on b5 b9)
(on b6 b7)
(ontable b7)
(on b8 b1)
(on b9 b2)
(on b10 b8)
(clear b4)
)
(:goal
(and
(on b2 b10)
(on b5 b1)
(on b6 b9)
(on b7 b4)
(on b8 b7)
(on b10 b6))
)
)


