(define (problem depot-3-3-3-6-6-3) (:domain depots)
(:objects
	depot0 depot1 depot2 - depot
	distributor0 distributor1 distributor2 - distributor
	truck0 truck1 truck2 - truck
	pallet0 pallet1 pallet2 pallet3 pallet4 pallet5 - pallet
	crate0 crate1 crate2 - crate
	hoist0 hoist1 hoist2 hoist3 hoist4 hoist5 - hoist)
(:init
	(at pallet0 depot0)
	(clear crate1)
	(at pallet1 depot1)
	(clear pallet1)
	(at pallet2 depot2)
	(clear crate2)
	(at pallet3 distributor0)
	(clear pallet3)
	(at pallet4 distributor1)
	(clear pallet4)
	(at pallet5 distributor2)
	(clear crate0)
	(at truck0 distributor1)
	(at truck1 depot2)
	(at truck2 depot2)
	(at hoist0 depot0)
	(available hoist0)
	(at hoist1 depot1)
	(available hoist1)
	(at hoist2 depot2)
	(available hoist2)
	(at hoist3 distributor0)
	(available hoist3)
	(at hoist4 distributor1)
	(available hoist4)
	(at hoist5 distributor2)
	(available hoist5)
	(at crate0 distributor2)
	(on crate0 pallet5)
	(at crate1 depot0)
	(on crate1 pallet0)
	(at crate2 depot2)
	(on crate2 pallet2)
)

(:goal (and
		(on crate1 pallet0)
		(on crate2 crate1)
	)
))
