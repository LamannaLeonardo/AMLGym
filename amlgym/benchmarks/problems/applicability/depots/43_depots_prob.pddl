(define (problem depot_2_3_2_5_5_2) (:domain depots)
(:objects
	depot0 depot1 - depot
	distributor0 distributor1 distributor2 - distributor
	truck0 truck1 - truck
	pallet0 pallet1 pallet2 pallet3 pallet4 - pallet
	crate0 crate1 - crate
	hoist0 hoist1 hoist2 hoist3 hoist4 - hoist)
(:init
	(at pallet0 depot0)
	(clear pallet0)
	(at pallet1 depot1)
	(clear crate1)
	(at pallet2 distributor0)
	(clear pallet2)
	(at pallet3 distributor1)
	(clear pallet3)
	(at pallet4 distributor2)
	(clear pallet4)
	(at truck0 distributor1)
	(at truck1 distributor0)
	(at hoist0 depot0)
	(available hoist0)
	(at hoist1 depot1)
	(available hoist1)
	(at hoist2 distributor0)
	(available hoist2)
	(at hoist3 distributor1)
	(available hoist3)
	(at hoist4 distributor2)
	(available hoist4)
	(at crate0 depot1)
	(on crate0 pallet1)
	(at crate1 depot1)
	(on crate1 crate0)
)

(:goal (and
		(on crate0 pallet4)
		(on crate1 pallet3)
	)
))
