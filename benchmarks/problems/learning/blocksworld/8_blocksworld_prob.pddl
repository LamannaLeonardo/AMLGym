

(define (problem bw_rand_11)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(on b1 b8)
(on b2 b6)
(on b3 b11)
(on b4 b3)
(on b5 b4)
(on b6 b1)
(on b7 b2)
(on b8 b9)
(ontable b9)
(on b10 b5)
(ontable b11)
(clear b7)
(clear b10)
)
(:goal
(and
(on b1 b4)
(on b2 b7)
(on b3 b11)
(on b4 b3)
(on b5 b8)
(on b6 b2)
(on b7 b10)
(on b9 b1))
)
)


