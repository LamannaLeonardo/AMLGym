
(define (problem transport-three-cities-sequential-6nodes-10size-3degree-10mindistance-1trucks-2packages-112seed)
 (:domain transport)
 (:objects
  city-1-loc-1 - location
  city-2-loc-1 - location
  city-3-loc-1 - location
  city-1-loc-2 - location
  city-2-loc-2 - location
  city-3-loc-2 - location
  city-1-loc-3 - location
  city-2-loc-3 - location
  city-3-loc-3 - location
  city-1-loc-4 - location
  city-2-loc-4 - location
  city-3-loc-4 - location
  city-1-loc-5 - location
  city-2-loc-5 - location
  city-3-loc-5 - location
  city-1-loc-6 - location
  city-2-loc-6 - location
  city-3-loc-6 - location
  truck-1 - vehicle
  package-1 - package
  package-2 - package
  capacity-0 - capacity-number
  capacity-1 - capacity-number
  capacity-2 - capacity-number
  capacity-3 - capacity-number
  capacity-4 - capacity-number
 )
 (:init
  
  (capacity-predecessor capacity-0 capacity-1)
  (capacity-predecessor capacity-1 capacity-2)
  (capacity-predecessor capacity-2 capacity-3)
  (capacity-predecessor capacity-3 capacity-4)
  (road city-1-loc-2 city-1-loc-1)
  (road city-1-loc-1 city-1-loc-2)
  (road city-1-loc-4 city-1-loc-3)
  (road city-1-loc-3 city-1-loc-4)
  (road city-1-loc-5 city-1-loc-1)
  (road city-1-loc-1 city-1-loc-5)
  (road city-1-loc-5 city-1-loc-2)
  (road city-1-loc-2 city-1-loc-5)
  (road city-1-loc-5 city-1-loc-3)
  (road city-1-loc-3 city-1-loc-5)
  (road city-1-loc-5 city-1-loc-4)
  (road city-1-loc-4 city-1-loc-5)
  (road city-1-loc-6 city-1-loc-3)
  (road city-1-loc-3 city-1-loc-6)
  (road city-2-loc-3 city-2-loc-1)
  (road city-2-loc-1 city-2-loc-3)
  (road city-2-loc-4 city-2-loc-3)
  (road city-2-loc-3 city-2-loc-4)
  (road city-2-loc-5 city-2-loc-4)
  (road city-2-loc-4 city-2-loc-5)
  (road city-2-loc-6 city-2-loc-2)
  (road city-2-loc-2 city-2-loc-6)
  (road city-2-loc-6 city-2-loc-5)
  (road city-2-loc-5 city-2-loc-6)
  (road city-3-loc-3 city-3-loc-1)
  (road city-3-loc-1 city-3-loc-3)
  (road city-3-loc-4 city-3-loc-1)
  (road city-3-loc-1 city-3-loc-4)
  (road city-3-loc-4 city-3-loc-2)
  (road city-3-loc-2 city-3-loc-4)
  (road city-3-loc-4 city-3-loc-3)
  (road city-3-loc-3 city-3-loc-4)
  (road city-3-loc-6 city-3-loc-2)
  (road city-3-loc-2 city-3-loc-6)
  (road city-3-loc-6 city-3-loc-4)
  (road city-3-loc-4 city-3-loc-6)
  (road city-3-loc-6 city-3-loc-5)
  (road city-3-loc-5 city-3-loc-6)
  (road city-1-loc-4 city-2-loc-6)
  (road city-2-loc-6 city-1-loc-4)
  (road city-1-loc-5 city-3-loc-5)
  (road city-3-loc-5 city-1-loc-5)
  (road city-2-loc-3 city-3-loc-5)
  (road city-3-loc-5 city-2-loc-3)
  (at package-1 city-2-loc-3)
  (at package-2 city-2-loc-4)
  (at truck-1 city-2-loc-3)
  (capacity truck-1 capacity-4)
 )
 (:goal (and
  (at package-1 city-3-loc-3)
  (at package-2 city-1-loc-6)
 ))
 
)
