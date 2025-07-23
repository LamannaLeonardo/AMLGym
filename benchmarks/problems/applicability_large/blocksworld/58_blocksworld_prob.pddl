

(define (problem bw_rand_11)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(ontable b1)
(on b2 b1)
(on b3 b5)
(on b4 b9)
(on b5 b7)
(on b6 b8)
(on b7 b6)
(on b8 b11)
(on b9 b2)
(on b10 b4)
(ontable b11)
(clear b3)
(clear b10)
)
(:goal
(and
(on b2 b8)
(on b3 b4)
(on b4 b5)
(on b5 b1)
(on b8 b6)
(on b9 b7)
(on b10 b11)
(on b11 b9))
)
)


