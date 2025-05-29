

(define (problem bw_rand_11)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(on b1 b10)
(ontable b2)
(on b3 b1)
(ontable b4)
(on b5 b3)
(ontable b6)
(on b7 b9)
(on b8 b5)
(on b9 b2)
(on b10 b7)
(ontable b11)
(clear b4)
(clear b6)
(clear b8)
(clear b11)
)
(:goal
(and
(on b1 b8)
(on b2 b3)
(on b3 b9)
(on b6 b4)
(on b7 b10)
(on b8 b11)
(on b11 b5))
)
)


