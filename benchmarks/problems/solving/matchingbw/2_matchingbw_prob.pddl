

(define (problem matching_bw_typed_n5)
(:domain matching_bw_typed)
(:requirements :typing)
(:objects h1 h2 - hand b1 b2 b3 b4 b5  - block)
(:init
 (empty h1)
 (empty h2)
 (hand_positive h1)
 (hand_negative h2)
 (solid b1)
 (block_positive b1)
 (on b1 b2)
 (solid b2)
 (block_positive b2)
 (on b2 b5)
 (solid b3)
 (block_negative b3)
 (on b3 b1)
 (solid b4)
 (block_negative b4)
 (on_table b4)
 (solid b5)
 (block_negative b5)
 (on_table b5)
 (clear b3)
 (clear b4)
)
(:goal
(and
 (on b1 b5)
 (on b4 b2))
)
)


