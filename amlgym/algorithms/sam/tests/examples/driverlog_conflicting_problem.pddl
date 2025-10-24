(define (problem dlog-2-2-3) (:domain driverlog)
(:objects
truck1 - truck
	truck2 - truck
	s2 - location
	s1 - location
	s0 - location
	p0-2 - location
	p0-1 - location
	p2-1 - location
	package1 - package
	package2 - package
	package3 - package
	driver2 - driver
	driver1 - driver
)

(:init
	(at driver1 s0)
	(at truck1 s0)
	(at package2 s1)
	(at driver2 s0)
	(at package3 s1)
	(at truck2 s1)
	(at package1 s2)
	(empty truck1)
	(empty truck2)
	(path p2-1 s2)
	(path p0-1 s1)
	(path s2 p0-2)
	(path p0-1 s0)
	(path s0 p0-2)
	(path p0-2 s2)
	(path s1 p0-1)
	(path s2 p2-1)
	(path p0-2 s0)
	(path s0 p0-1)
	(path s1 p2-1)
	(path p2-1 s1)
	(link s1 s2)
	(link s0 s2)
	(link s2 s0)
	(link s2 s1)
	(link s0 s1)
	(link s1 s0)

)

(:goal
	(and
	(at truck2 s0)
	(at truck1 s2)
	(at package2 s2)
	(at package1 s0)
	(at package3 s0)
	(dummy-additional-predicate )
)
)

)