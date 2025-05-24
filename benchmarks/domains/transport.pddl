;; transport sequential
;;

(define (domain transport)
  (:requirements :typing)
  (:types
        location target locatable - object
        vehicle package - locatable
        capacity_number - object
  )

  (:predicates 
     (road ?l1 ?l2 - location)
     (at ?x - locatable ?v - location)
     (in ?x - package ?v - vehicle)
     (capacity ?v - vehicle ?s1 - capacity_number)
     (capacity_predecessor ?s1 ?s2 - capacity_number)
  )


  (:action drive
    :parameters (?v - vehicle ?l1 ?l2 - location)
    :precondition (and
        (at ?v ?l1)
        (road ?l1 ?l2)
      )
    :effect (and
        (not (at ?v ?l1))
        (at ?v ?l2)
      )
  )

 (:action pick_up
    :parameters (?v - vehicle ?l - location ?p - package ?s1 ?s2 - capacity_number)
    :precondition (and
        (at ?v ?l)
        (at ?p ?l)
        (capacity_predecessor ?s1 ?s2)
        (capacity ?v ?s2)
      )
    :effect (and
        (not (at ?p ?l))
        (in ?p ?v)
        (capacity ?v ?s1)
        (not (capacity ?v ?s2))
      )
  )

  (:action drop
    :parameters (?v - vehicle ?l - location ?p - package ?s1 ?s2 - capacity_number)
    :precondition (and
        (at ?v ?l)
        (in ?p ?v)
        (capacity_predecessor ?s1 ?s2)
        (capacity ?v ?s1)
      )
    :effect (and
        (not (in ?p ?v))
        (at ?p ?l)
        (capacity ?v ?s2)
        (not (capacity ?v ?s1))
      )
  )

)
