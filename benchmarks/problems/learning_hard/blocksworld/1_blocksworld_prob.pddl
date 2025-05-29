

(define (problem bw_rand_12)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b6)
(on b2 b3)
(ontable b3)
(on b4 b12)
(on b5 b4)
(ontable b6)
(on b7 b11)
(ontable b8)
(ontable b9)
(on b10 b1)
(on b11 b5)
(on b12 b10)
(clear b2)
(clear b7)
(clear b8)
(clear b9)
)
(:goal
(and
(on b1 b12)
(on b2 b7)
(on b4 b10)
(on b8 b2)
(on b9 b4)
(on b11 b3))
)
)


