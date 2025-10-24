

(define (problem matching_bw_typed_n4)
(:domain matching_bw_typed)
(:requirements :typing)
(:objects h1 h2 - hand b1 b2 b3 b4  - block)
(:init
 (empty h1)
 (empty h2)
 (hand_positive h1)
 (hand_negative h2)
 (solid b1)
 (block_positive b1)
 (on_table b1)
 (solid b2)
 (block_positive b2)
 (on b2 b4)
 (solid b3)
 (block_negative b3)
 (on b3 b2)
 (solid b4)
 (block_negative b4)
 (on b4 b1)
 (clear b3)
)
(:goal
(and
 (on b1 b4)
 (on b2 b3)
 (on b4 b2))
)
)


