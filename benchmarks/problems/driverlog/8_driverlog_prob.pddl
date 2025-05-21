(define (problem dlog-7-5-9)
	(:domain driverlog)
	(:objects
	driver1 - driver
	driver2 - driver
	driver3 - driver
	driver4 - driver
	driver5 - driver
	driver6 - driver
	driver7 - driver
	truck1 - truck
	truck2 - truck
	truck3 - truck
	truck4 - truck
	truck5 - truck
	package1 - obj
	package2 - obj
	package3 - obj
	package4 - obj
	package5 - obj
	package6 - obj
	package7 - obj
	package8 - obj
	package9 - obj
	s0 - location
	s1 - location
	s2 - location
	s3 - location
	s4 - location
	s5 - location
	p1-0 - location
	p1-2 - location
	p1-5 - location
	p2-0 - location
	p2-3 - location
	p3-2 - location
	p3-4 - location
	p4-1 - location
	p4-2 - location
	p5-0 - location
	p5-1 - location
	)
	(:init
	(at driver1 s1)
	(at driver2 s4)
	(at driver3 s3)
	(at driver4 s1)
	(at driver5 s2)
	(at driver6 s5)
	(at driver7 s5)
	(at truck1 s1)
	(empty truck1)
	(at truck2 s1)
	(empty truck2)
	(at truck3 s2)
	(empty truck3)
	(at truck4 s5)
	(empty truck4)
	(at truck5 s5)
	(empty truck5)
	(at package1 s3)
	(at package2 s2)
	(at package3 s4)
	(at package4 s3)
	(at package5 s3)
	(at package6 s5)
	(at package7 s3)
	(at package8 s3)
	(at package9 s2)
	(path s1 p1-0)
	(path p1-0 s1)
	(path s0 p1-0)
	(path p1-0 s0)
	(path s1 p1-2)
	(path p1-2 s1)
	(path s2 p1-2)
	(path p1-2 s2)
	(path s1 p1-5)
	(path p1-5 s1)
	(path s5 p1-5)
	(path p1-5 s5)
	(path s2 p2-0)
	(path p2-0 s2)
	(path s0 p2-0)
	(path p2-0 s0)
	(path s2 p2-3)
	(path p2-3 s2)
	(path s3 p2-3)
	(path p2-3 s3)
	(path s3 p3-4)
	(path p3-4 s3)
	(path s4 p3-4)
	(path p3-4 s4)
	(path s4 p4-1)
	(path p4-1 s4)
	(path s1 p4-1)
	(path p4-1 s1)
	(path s4 p4-2)
	(path p4-2 s4)
	(path s2 p4-2)
	(path p4-2 s2)
	(path s5 p5-0)
	(path p5-0 s5)
	(path s0 p5-0)
	(path p5-0 s0)
	(link s0 s2)
	(link s2 s0)
	(link s0 s3)
	(link s3 s0)
	(link s0 s5)
	(link s5 s0)
	(link s1 s0)
	(link s0 s1)
	(link s1 s4)
	(link s4 s1)
	(link s2 s1)
	(link s1 s2)
	(link s3 s1)
	(link s1 s3)
	(link s3 s2)
	(link s2 s3)
	(link s3 s4)
	(link s4 s3)
	(link s3 s5)
	(link s5 s3)
)
	(:goal (and
	(at driver2 s1)
	(at driver3 s3)
	(at driver4 s3)
	(at driver5 s1)
	(at driver6 s3)
	(at driver7 s1)
	(at truck1 s1)
	(at truck2 s4)
	(at truck3 s0)
	(at truck4 s1)
	(at truck5 s0)
	(at package1 s3)
	(at package2 s5)
	(at package3 s1)
	(at package4 s1)
	(at package5 s1)
	(at package6 s2)
	(at package7 s4)
	(at package8 s1)
	(at package9 s0)
	))



)
