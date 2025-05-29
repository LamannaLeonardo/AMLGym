(define (problem depot_2_2_2_4_4_2) (:domain depots)
(:objects
	depot0 depot1 - depot
	distributor0 distributor1 - distributor
	truck0 truck1 - truck
	pallet0 pallet1 pallet2 pallet3 - pallet
	crate0 crate1 - crate
	hoist0 hoist1 hoist2 hoist3 - hoist)
(:init
	(at pallet0 depot0)
	(clear pallet0)
	(at pallet1 depot1)
	(clear pallet1)
	(at pallet2 distributor0)
	(clear crate0)
	(at pallet3 distributor1)
	(clear crate1)
	(at truck0 distributor1)
	(at truck1 depot1)
	(at hoist0 depot0)
	(available hoist0)
	(at hoist1 depot1)
	(available hoist1)
	(at hoist2 distributor0)
	(available hoist2)
	(at hoist3 distributor1)
	(available hoist3)
	(at crate0 distributor0)
	(on crate0 pallet2)
	(at crate1 distributor1)
	(on crate1 pallet3)
)

(:goal (and
		(on crate0 crate1)
		(on crate1 pallet2)
	)
))
