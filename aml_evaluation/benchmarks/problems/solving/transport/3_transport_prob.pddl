
(define (problem transport_city_sequential_8nodes_10size_3degree_10mindistance_2trucks_4packages_211seed)
 (:domain transport)
 (:objects
  city_loc_1 - location
  city_loc_2 - location
  city_loc_3 - location
  city_loc_4 - location
  city_loc_5 - location
  city_loc_6 - location
  city_loc_7 - location
  city_loc_8 - location
  truck_1 - vehicle
  truck_2 - vehicle
  package_1 - package
  package_2 - package
  package_3 - package
  package_4 - package
  capacity_0 - capacity_number
  capacity_1 - capacity_number
  capacity_2 - capacity_number
  capacity_3 - capacity_number
  capacity_4 - capacity_number
 )
 (:init
  
  (capacity_predecessor capacity_0 capacity_1)
  (capacity_predecessor capacity_1 capacity_2)
  (capacity_predecessor capacity_2 capacity_3)
  (capacity_predecessor capacity_3 capacity_4)
  (road city_loc_2 city_loc_1)
  (road city_loc_1 city_loc_2)
  (road city_loc_3 city_loc_1)
  (road city_loc_1 city_loc_3)
  (road city_loc_3 city_loc_2)
  (road city_loc_2 city_loc_3)
  (road city_loc_5 city_loc_2)
  (road city_loc_2 city_loc_5)
  (road city_loc_5 city_loc_3)
  (road city_loc_3 city_loc_5)
  (road city_loc_6 city_loc_1)
  (road city_loc_1 city_loc_6)
  (road city_loc_7 city_loc_2)
  (road city_loc_2 city_loc_7)
  (road city_loc_8 city_loc_2)
  (road city_loc_2 city_loc_8)
  (road city_loc_8 city_loc_4)
  (road city_loc_4 city_loc_8)
  (road city_loc_8 city_loc_7)
  (road city_loc_7 city_loc_8)
  (at package_1 city_loc_1)
  (at package_2 city_loc_6)
  (at package_3 city_loc_2)
  (at package_4 city_loc_2)
  (at truck_1 city_loc_8)
  (capacity truck_1 capacity_2)
  (at truck_2 city_loc_3)
  (capacity truck_2 capacity_3)
 )
 (:goal (and
  (at package_1 city_loc_3)
  (at package_2 city_loc_4)
  (at package_3 city_loc_1)
  (at package_4 city_loc_3)
 ))
 
)
