(define (problem grid_8)
(:domain grid_visit_all)
(:objects 
	loc_x0_y0
	loc_x0_y1
	loc_x0_y7
	loc_x1_y5
	loc_x1_y6
	loc_x1_y7
	loc_x2_y3
	loc_x2_y4
	loc_x2_y5
	loc_x2_y6
	loc_x3_y1
	loc_x3_y2
	loc_x3_y3
	loc_x3_y5
	loc_x3_y6
	loc_x4_y1
	loc_x4_y3
	loc_x4_y4
	loc_x4_y6
	loc_x5_y1
	loc_x6_y0
	loc_x6_y1
	loc_x6_y2
	loc_x6_y3
	loc_x6_y4
	loc_x6_y6
	loc_x6_y7
	loc_x7_y1
	loc_x7_y3
- place 
        
)
(:init
	(at_robot loc_x4_y6)
	(visited loc_x4_y6)
	(connected loc_x0_y0 loc_x0_y1)
 	(connected loc_x0_y1 loc_x0_y0)
 	(connected loc_x0_y7 loc_x1_y7)
 	(connected loc_x1_y5 loc_x2_y5)
 	(connected loc_x1_y5 loc_x1_y6)
 	(connected loc_x1_y6 loc_x2_y6)
 	(connected loc_x1_y6 loc_x1_y5)
 	(connected loc_x1_y6 loc_x1_y7)
 	(connected loc_x1_y7 loc_x0_y7)
 	(connected loc_x1_y7 loc_x1_y6)
 	(connected loc_x2_y3 loc_x3_y3)
 	(connected loc_x2_y3 loc_x2_y4)
 	(connected loc_x2_y4 loc_x2_y3)
 	(connected loc_x2_y4 loc_x2_y5)
 	(connected loc_x2_y5 loc_x1_y5)
 	(connected loc_x2_y5 loc_x3_y5)
 	(connected loc_x2_y5 loc_x2_y4)
 	(connected loc_x2_y5 loc_x2_y6)
 	(connected loc_x2_y6 loc_x1_y6)
 	(connected loc_x2_y6 loc_x3_y6)
 	(connected loc_x2_y6 loc_x2_y5)
 	(connected loc_x3_y1 loc_x4_y1)
 	(connected loc_x3_y1 loc_x3_y2)
 	(connected loc_x3_y2 loc_x3_y1)
 	(connected loc_x3_y2 loc_x3_y3)
 	(connected loc_x3_y3 loc_x2_y3)
 	(connected loc_x3_y3 loc_x4_y3)
 	(connected loc_x3_y3 loc_x3_y2)
 	(connected loc_x3_y5 loc_x2_y5)
 	(connected loc_x3_y5 loc_x3_y6)
 	(connected loc_x3_y6 loc_x2_y6)
 	(connected loc_x3_y6 loc_x4_y6)
 	(connected loc_x3_y6 loc_x3_y5)
 	(connected loc_x4_y1 loc_x3_y1)
 	(connected loc_x4_y1 loc_x5_y1)
 	(connected loc_x4_y3 loc_x3_y3)
 	(connected loc_x4_y3 loc_x4_y4)
 	(connected loc_x4_y4 loc_x4_y3)
 	(connected loc_x4_y6 loc_x3_y6)
 	(connected loc_x5_y1 loc_x4_y1)
 	(connected loc_x5_y1 loc_x6_y1)
 	(connected loc_x6_y0 loc_x6_y1)
 	(connected loc_x6_y1 loc_x5_y1)
 	(connected loc_x6_y1 loc_x7_y1)
 	(connected loc_x6_y1 loc_x6_y0)
 	(connected loc_x6_y1 loc_x6_y2)
 	(connected loc_x6_y2 loc_x6_y1)
 	(connected loc_x6_y2 loc_x6_y3)
 	(connected loc_x6_y3 loc_x7_y3)
 	(connected loc_x6_y3 loc_x6_y2)
 	(connected loc_x6_y3 loc_x6_y4)
 	(connected loc_x6_y4 loc_x6_y3)
 	(connected loc_x6_y6 loc_x6_y7)
 	(connected loc_x6_y7 loc_x6_y6)
 	(connected loc_x7_y1 loc_x6_y1)
 	(connected loc_x7_y3 loc_x6_y3)
 
)
(:goal
(and 
	(visited loc_x0_y7)
	(visited loc_x1_y6)
	(visited loc_x2_y4)
	(visited loc_x2_y5)
	(visited loc_x3_y1)
	(visited loc_x3_y2)
	(visited loc_x3_y5)
	(visited loc_x3_y6)
	(visited loc_x4_y4)
	(visited loc_x4_y6)
	(visited loc_x6_y3)
	(visited loc_x6_y4)
	(visited loc_x7_y1)
	(visited loc_x7_y3)
)
)
)
