

(define (problem bw_rand_12)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(ontable b1)
(ontable b2)
(on b3 b10)
(on b4 b9)
(on b5 b11)
(on b6 b3)
(on b7 b2)
(on b8 b1)
(on b9 b12)
(on b10 b5)
(on b11 b7)
(on b12 b6)
(clear b4)
(clear b8)
)
(:goal
(and
(on b1 b11)
(on b2 b4)
(on b3 b9)
(on b4 b3)
(on b7 b5)
(on b8 b2)
(on b9 b1)
(on b10 b7)
(on b11 b6)
(on b12 b8))
)
)


