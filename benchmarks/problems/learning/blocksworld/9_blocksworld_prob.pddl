

(define (problem bw_rand_12)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b6)
(on b2 b8)
(ontable b3)
(on b4 b1)
(on b5 b9)
(on b6 b3)
(on b7 b5)
(on b8 b11)
(on b9 b4)
(ontable b10)
(ontable b11)
(on b12 b2)
(clear b7)
(clear b10)
(clear b12)
)
(:goal
(and
(on b1 b6)
(on b2 b1)
(on b3 b2)
(on b4 b5)
(on b5 b11)
(on b6 b8)
(on b8 b7)
(on b10 b9)
(on b12 b4))
)
)


