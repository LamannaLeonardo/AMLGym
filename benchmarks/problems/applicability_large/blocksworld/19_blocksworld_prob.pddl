

(define (problem bw_rand_12)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b2)
(ontable b2)
(on b3 b6)
(on b4 b7)
(on b5 b10)
(on b6 b8)
(on b7 b12)
(on b8 b5)
(on b9 b3)
(ontable b10)
(on b11 b1)
(on b12 b11)
(clear b4)
(clear b9)
)
(:goal
(and
(on b1 b5)
(on b3 b7)
(on b4 b8)
(on b7 b6)
(on b8 b11)
(on b10 b4)
(on b11 b12)
(on b12 b2))
)
)


