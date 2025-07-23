

(define (problem bw_rand_12)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b12)
(ontable b2)
(on b3 b6)
(ontable b4)
(on b5 b11)
(on b6 b5)
(on b7 b2)
(on b8 b10)
(ontable b9)
(on b10 b4)
(on b11 b1)
(on b12 b7)
(clear b3)
(clear b8)
(clear b9)
)
(:goal
(and
(on b1 b4)
(on b2 b5)
(on b3 b9)
(on b4 b8)
(on b5 b11)
(on b7 b10)
(on b8 b7)
(on b9 b6)
(on b11 b3)
(on b12 b2))
)
)


