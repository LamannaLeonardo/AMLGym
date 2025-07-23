(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	satellite1 - satellite
	instrument2 - instrument
	instrument3 - instrument
	satellite2 - satellite
	instrument4 - instrument
	satellite3 - satellite
	instrument5 - instrument
	satellite4 - satellite
	instrument6 - instrument
	instrument7 - instrument
	thermograph2 - mode
	thermograph0 - mode
	thermograph1 - mode
	star3 - direction
	groundstation0 - direction
	star1 - direction
	groundstation2 - direction
	phenomenon4 - direction
	planet5 - direction
	planet6 - direction
	star7 - direction
	star8 - direction
	phenomenon9 - direction
)
(:init
	(supports instrument0 thermograph2)
	(supports instrument0 thermograph0)
	(calibration_target instrument0 star3)
	(supports instrument1 thermograph0)
	(supports instrument1 thermograph2)
	(supports instrument1 thermograph1)
	(calibration_target instrument1 star1)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 planet6)
	(supports instrument2 thermograph2)
	(supports instrument2 thermograph0)
	(supports instrument2 thermograph1)
	(calibration_target instrument2 groundstation2)
	(supports instrument3 thermograph0)
	(supports instrument3 thermograph1)
	(calibration_target instrument3 groundstation0)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(power_avail satellite1)
	(pointing satellite1 planet5)
	(supports instrument4 thermograph2)
	(supports instrument4 thermograph0)
	(calibration_target instrument4 groundstation0)
	(on_board instrument4 satellite2)
	(power_avail satellite2)
	(pointing satellite2 phenomenon4)
	(supports instrument5 thermograph2)
	(supports instrument5 thermograph0)
	(calibration_target instrument5 star1)
	(on_board instrument5 satellite3)
	(power_avail satellite3)
	(pointing satellite3 groundstation2)
	(supports instrument6 thermograph2)
	(supports instrument6 thermograph0)
	(calibration_target instrument6 star1)
	(supports instrument7 thermograph0)
	(supports instrument7 thermograph2)
	(calibration_target instrument7 groundstation2)
	(on_board instrument6 satellite4)
	(on_board instrument7 satellite4)
	(power_avail satellite4)
	(pointing satellite4 star1)
)
(:goal (and
	(pointing satellite0 phenomenon4)
	(pointing satellite2 star3)
	(pointing satellite4 star7)
	(have_image phenomenon4 thermograph2)
	(have_image planet5 thermograph0)
	(have_image planet6 thermograph1)
	(have_image star7 thermograph2)
	(have_image star8 thermograph0)
	(have_image phenomenon9 thermograph1)
))

)
