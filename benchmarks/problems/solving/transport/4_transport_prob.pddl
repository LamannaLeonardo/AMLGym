
(define (problem transport_two_cities_sequential_8nodes_10size_3degree_10mindistance_2trucks_4packages_898seed)
 (:domain transport)
 (:objects
  city_1_loc_1 - location
  city_2_loc_1 - location
  city_1_loc_2 - location
  city_2_loc_2 - location
  city_1_loc_3 - location
  city_2_loc_3 - location
  city_1_loc_4 - location
  city_2_loc_4 - location
  city_1_loc_5 - location
  city_2_loc_5 - location
  city_1_loc_6 - location
  city_2_loc_6 - location
  city_1_loc_7 - location
  city_2_loc_7 - location
  city_1_loc_8 - location
  city_2_loc_8 - location
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
  (road city_1_loc_2 city_1_loc_1)
  (road city_1_loc_1 city_1_loc_2)
  (road city_1_loc_3 city_1_loc_1)
  (road city_1_loc_1 city_1_loc_3)
  (road city_1_loc_6 city_1_loc_4)
  (road city_1_loc_4 city_1_loc_6)
  (road city_1_loc_6 city_1_loc_5)
  (road city_1_loc_5 city_1_loc_6)
  (road city_1_loc_7 city_1_loc_4)
  (road city_1_loc_4 city_1_loc_7)
  (road city_1_loc_7 city_1_loc_6)
  (road city_1_loc_6 city_1_loc_7)
  (road city_1_loc_8 city_1_loc_3)
  (road city_1_loc_3 city_1_loc_8)
  (road city_1_loc_8 city_1_loc_4)
  (road city_1_loc_4 city_1_loc_8)
  (road city_2_loc_4 city_2_loc_1)
  (road city_2_loc_1 city_2_loc_4)
  (road city_2_loc_5 city_2_loc_3)
  (road city_2_loc_3 city_2_loc_5)
  (road city_2_loc_6 city_2_loc_1)
  (road city_2_loc_1 city_2_loc_6)
  (road city_2_loc_6 city_2_loc_5)
  (road city_2_loc_5 city_2_loc_6)
  (road city_2_loc_7 city_2_loc_1)
  (road city_2_loc_1 city_2_loc_7)
  (road city_2_loc_7 city_2_loc_2)
  (road city_2_loc_2 city_2_loc_7)
  (road city_2_loc_7 city_2_loc_4)
  (road city_2_loc_4 city_2_loc_7)
  (road city_2_loc_8 city_2_loc_2)
  (road city_2_loc_2 city_2_loc_8)
  (road city_2_loc_8 city_2_loc_7)
  (road city_2_loc_7 city_2_loc_8)
  (road city_1_loc_4 city_2_loc_1)
  (road city_2_loc_1 city_1_loc_4)
  (at package_1 city_1_loc_8)
  (at package_2 city_1_loc_4)
  (at package_3 city_1_loc_7)
  (at package_4 city_1_loc_5)
  (at truck_1 city_2_loc_1)
  (capacity truck_1 capacity_3)
  (at truck_2 city_2_loc_6)
  (capacity truck_2 capacity_2)
 )
 (:goal (and
  (at package_1 city_2_loc_4)
  (at package_2 city_2_loc_5)
  (at package_3 city_2_loc_3)
  (at package_4 city_2_loc_1)
 ))
 
)
