(define (problem grid_3)
(:domain grid_visit_all)
(:objects 
	loc_x0_y1
	loc_x0_y2
	loc_x0_y3
	loc_x1_y2
	loc_x1_y3
	loc_x2_y0
	loc_x2_y2
	loc_x2_y3
- place 
        
)
(:init
	(at_robot loc_x1_y3)
	(visited loc_x1_y3)
	(connected loc_x0_y1 loc_x0_y2)
 	(connected loc_x0_y2 loc_x1_y2)
 	(connected loc_x0_y2 loc_x0_y1)
 	(connected loc_x0_y2 loc_x0_y3)
 	(connected loc_x0_y3 loc_x1_y3)
 	(connected loc_x0_y3 loc_x0_y2)
 	(connected loc_x1_y2 loc_x0_y2)
 	(connected loc_x1_y2 loc_x2_y2)
 	(connected loc_x1_y2 loc_x1_y3)
 	(connected loc_x1_y3 loc_x0_y3)
 	(connected loc_x1_y3 loc_x2_y3)
 	(connected loc_x1_y3 loc_x1_y2)
 	(connected loc_x2_y2 loc_x1_y2)
 	(connected loc_x2_y2 loc_x2_y3)
 	(connected loc_x2_y3 loc_x1_y3)
 	(connected loc_x2_y3 loc_x2_y2)
 
)
(:goal
(and 
	(visited loc_x0_y1)
	(visited loc_x0_y2)
	(visited loc_x0_y3)
	(visited loc_x1_y2)
	(visited loc_x1_y3)
)
)
)
