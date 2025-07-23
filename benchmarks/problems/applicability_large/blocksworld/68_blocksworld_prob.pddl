

(define (problem bw_rand_11)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(on b1 b3)
(ontable b2)
(on b3 b2)
(on b4 b5)
(on b5 b8)
(on b6 b11)
(on b7 b4)
(on b8 b6)
(on b9 b10)
(on b10 b7)
(on b11 b1)
(clear b9)
)
(:goal
(and
(on b1 b9)
(on b2 b3)
(on b3 b5)
(on b4 b11)
(on b7 b6)
(on b8 b10)
(on b9 b2)
(on b10 b1)
(on b11 b8))
)
)


