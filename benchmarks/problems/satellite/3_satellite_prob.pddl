(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	instrument2 - instrument
	satellite2 - satellite
	instrument3 - instrument
	satellite3 - satellite
	instrument4 - instrument
	thermograph1 - mode
	thermograph0 - mode
	thermograph2 - mode
	star2 - direction
	groundstation1 - direction
	groundstation0 - direction
	star3 - direction
	planet4 - direction
	star5 - direction
	planet6 - direction
	phenomenon7 - direction
)
(:init
	(supports instrument0 thermograph1)
	(calibration_target instrument0 groundstation1)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 groundstation1)
	(supports instrument1 thermograph1)
	(supports instrument1 thermograph2)
	(calibration_target instrument1 groundstation1)
	(supports instrument2 thermograph2)
	(calibration_target instrument2 star2)
	(on_board instrument1 satellite1)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 groundstation1)
	(supports instrument3 thermograph2)
	(supports instrument3 thermograph1)
	(supports instrument3 thermograph0)
	(calibration_target instrument3 groundstation1)
	(on_board instrument3 satellite2)
	(power_avail satellite2)
	(pointing satellite2 planet6)
	(supports instrument4 thermograph0)
	(calibration_target instrument4 groundstation0)
	(on_board instrument4 satellite3)
	(power_avail satellite3)
	(pointing satellite3 groundstation0)
)
(:goal (and
	(pointing satellite3 star3)
	(have_image star3 thermograph2)
	(have_image planet4 thermograph2)
	(have_image star5 thermograph0)
	(have_image planet6 thermograph1)
	(have_image phenomenon7 thermograph2)
))

)
