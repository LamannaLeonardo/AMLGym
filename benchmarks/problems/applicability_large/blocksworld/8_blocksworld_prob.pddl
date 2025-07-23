

(define (problem bw_rand_11)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(ontable b1)
(on b2 b9)
(ontable b3)
(on b4 b1)
(on b5 b8)
(on b6 b11)
(on b7 b2)
(on b8 b3)
(on b9 b10)
(ontable b10)
(on b11 b5)
(clear b4)
(clear b6)
(clear b7)
)
(:goal
(and
(on b1 b7)
(on b2 b8)
(on b3 b1)
(on b4 b2)
(on b5 b4)
(on b8 b10)
(on b10 b9)
(on b11 b5))
)
)


