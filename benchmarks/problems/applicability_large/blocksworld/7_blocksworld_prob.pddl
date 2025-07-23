

(define (problem bw_rand_10)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b6)
(on b2 b8)
(on b3 b5)
(ontable b4)
(on b5 b1)
(ontable b6)
(ontable b7)
(ontable b8)
(ontable b9)
(on b10 b4)
(clear b2)
(clear b3)
(clear b7)
(clear b9)
(clear b10)
)
(:goal
(and
(on b1 b5)
(on b2 b8)
(on b3 b7)
(on b4 b3)
(on b5 b4)
(on b6 b2)
(on b7 b6)
(on b8 b10)
(on b9 b1))
)
)


