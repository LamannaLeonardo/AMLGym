

(define (problem bw_rand_11)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(ontable b1)
(on b2 b11)
(on b3 b1)
(on b4 b3)
(on b5 b2)
(on b6 b5)
(ontable b7)
(on b8 b4)
(on b9 b8)
(on b10 b9)
(on b11 b10)
(clear b6)
(clear b7)
)
(:goal
(and
(on b1 b6)
(on b3 b8)
(on b4 b10)
(on b5 b4)
(on b6 b9)
(on b7 b5)
(on b8 b11)
(on b9 b3)
(on b11 b7))
)
)


