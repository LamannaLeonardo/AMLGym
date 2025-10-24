
(define (problem transport_three_cities_sequential_6nodes_10size_3degree_10mindistance_1trucks_2packages_407seed)
 (:domain transport)
 (:objects
  city_1_loc_1 - location
  city_2_loc_1 - location
  city_3_loc_1 - location
  city_1_loc_2 - location
  city_2_loc_2 - location
  city_3_loc_2 - location
  city_1_loc_3 - location
  city_2_loc_3 - location
  city_3_loc_3 - location
  city_1_loc_4 - location
  city_2_loc_4 - location
  city_3_loc_4 - location
  city_1_loc_5 - location
  city_2_loc_5 - location
  city_3_loc_5 - location
  city_1_loc_6 - location
  city_2_loc_6 - location
  city_3_loc_6 - location
  truck_1 - vehicle
  package_1 - package
  package_2 - package
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
  (road city_1_loc_3 city_1_loc_1)
  (road city_1_loc_1 city_1_loc_3)
  (road city_1_loc_4 city_1_loc_1)
  (road city_1_loc_1 city_1_loc_4)
  (road city_1_loc_5 city_1_loc_1)
  (road city_1_loc_1 city_1_loc_5)
  (road city_1_loc_6 city_1_loc_2)
  (road city_1_loc_2 city_1_loc_6)
  (road city_1_loc_6 city_1_loc_3)
  (road city_1_loc_3 city_1_loc_6)
  (road city_2_loc_3 city_2_loc_1)
  (road city_2_loc_1 city_2_loc_3)
  (road city_2_loc_4 city_2_loc_2)
  (road city_2_loc_2 city_2_loc_4)
  (road city_2_loc_5 city_2_loc_4)
  (road city_2_loc_4 city_2_loc_5)
  (road city_2_loc_6 city_2_loc_1)
  (road city_2_loc_1 city_2_loc_6)
  (road city_2_loc_6 city_2_loc_5)
  (road city_2_loc_5 city_2_loc_6)
  (road city_3_loc_2 city_3_loc_1)
  (road city_3_loc_1 city_3_loc_2)
  (road city_3_loc_3 city_3_loc_2)
  (road city_3_loc_2 city_3_loc_3)
  (road city_3_loc_4 city_3_loc_1)
  (road city_3_loc_1 city_3_loc_4)
  (road city_3_loc_5 city_3_loc_1)
  (road city_3_loc_1 city_3_loc_5)
  (road city_3_loc_6 city_3_loc_1)
  (road city_3_loc_1 city_3_loc_6)
  (road city_3_loc_6 city_3_loc_5)
  (road city_3_loc_5 city_3_loc_6)
  (road city_1_loc_6 city_2_loc_3)
  (road city_2_loc_3 city_1_loc_6)
  (road city_1_loc_3 city_3_loc_3)
  (road city_3_loc_3 city_1_loc_3)
  (road city_2_loc_6 city_3_loc_6)
  (road city_3_loc_6 city_2_loc_6)
  (at package_1 city_3_loc_1)
  (at package_2 city_2_loc_3)
  (at truck_1 city_3_loc_1)
  (capacity truck_1 capacity_4)
 )
 (:goal (and
  (at package_1 city_1_loc_1)
  (at package_2 city_3_loc_3)
 ))
 
)
