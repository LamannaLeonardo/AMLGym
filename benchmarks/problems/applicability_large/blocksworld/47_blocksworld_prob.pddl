

(define (problem bw_rand_10)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(ontable b1)
(ontable b2)
(on b3 b5)
(on b4 b9)
(on b5 b2)
(ontable b6)
(on b7 b10)
(on b8 b7)
(on b9 b6)
(ontable b10)
(clear b1)
(clear b3)
(clear b4)
(clear b8)
)
(:goal
(and
(on b1 b2)
(on b3 b7)
(on b5 b8)
(on b7 b6)
(on b8 b1)
(on b9 b4)
(on b10 b3))
)
)


