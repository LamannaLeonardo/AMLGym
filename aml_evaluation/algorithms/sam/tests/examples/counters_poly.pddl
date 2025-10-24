(define (domain fo-counters-rnd)
     (:requirements :strips :typing :fluents :equality)
     (:types
          counter
     )
     (:predicates
          (nop ?x - counter)
     )

     (:functions
          (value ?c - counter);; - int  ;; The value shown in counter ?c
          (max_int);; -  int ;; The maximum integer we consider - a static value
     )

     ;; Increment the value in the given counter by one
     (:action increment
          :parameters (?c - counter)
          :precondition (and (<= (+ (value ?c) 1) (max_int)))
          :effect (and (increase (value ?c) 1))
     )
     ;; Decrement the value in the given counter by one
     (:action decrement
          :parameters (?c - counter)
          :precondition (and (>= (- (value ?c) 1) 0))
          :effect (and (decrease (value ?c) 1))
     )

     (:action increment_by_counter
          :parameters (?c1 - counter ?c2 - counter)
          :precondition (and
               (not (= ?c1 ?c2))
               (<= (+ (value ?c1) (value ?c2)) (max_int)))
          :effect (and (increase (value ?c1) (value ?c2)))
     )

     (:action decrement_by_counter
          :parameters (?c1 - counter ?c2 - counter)
          :precondition (and 
               (not (= ?c1 ?c2))
               (>= (- (value ?c1) (value ?c2)) 0))
          :effect (and (decrease (value ?c1) (value ?c2)))
     )

     (:action multiply_by_counter
          :parameters (?c1 - counter ?c2 - counter ?c3 - counter)
          :precondition (and 
               (not (= ?c1 ?c2))
               (not (= ?c1 ?c3))
               (not (= ?c2 ?c3))
               (<= (* (value ?c2) (value ?c3)) (max_int)))
          :effect (and (assign (value ?c1) (* (value ?c2) (value ?c3))))
     )

)