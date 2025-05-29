(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	satellite2 - satellite
	instrument2 - instrument
	satellite3 - satellite
	instrument3 - instrument
	satellite4 - satellite
	instrument4 - instrument
	instrument5 - instrument
	satellite5 - satellite
	instrument6 - instrument
	instrument7 - instrument
	thermograph0 - mode
	thermograph1 - mode
	thermograph2 - mode
	thermograph4 - mode
	infrared3 - mode
	star1 - direction
	groundstation3 - direction
	groundstation0 - direction
	star4 - direction
	groundstation2 - direction
	planet5 - direction
	star6 - direction
	phenomenon7 - direction
	star8 - direction
	planet9 - direction
	star10 - direction
	phenomenon11 - direction
)
(:init
	(supports instrument0 thermograph4)
	(supports instrument0 thermograph0)
	(calibration_target instrument0 groundstation3)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star8)
	(supports instrument1 thermograph2)
	(calibration_target instrument1 groundstation3)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 groundstation0)
	(supports instrument2 thermograph0)
	(supports instrument2 thermograph2)
	(supports instrument2 thermograph4)
	(calibration_target instrument2 groundstation3)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 groundstation2)
	(supports instrument3 thermograph0)
	(supports instrument3 thermograph2)
	(calibration_target instrument3 groundstation0)
	(on_board instrument3 satellite3)
	(power_avail satellite3)
	(pointing satellite3 planet9)
	(supports instrument4 thermograph2)
	(supports instrument4 infrared3)
	(calibration_target instrument4 groundstation2)
	(supports instrument5 thermograph4)
	(supports instrument5 thermograph1)
	(supports instrument5 infrared3)
	(calibration_target instrument5 groundstation0)
	(on_board instrument4 satellite4)
	(on_board instrument5 satellite4)
	(power_avail satellite4)
	(pointing satellite4 groundstation0)
	(supports instrument6 thermograph0)
	(calibration_target instrument6 star4)
	(supports instrument7 thermograph2)
	(supports instrument7 thermograph4)
	(supports instrument7 thermograph1)
	(calibration_target instrument7 groundstation2)
	(on_board instrument6 satellite5)
	(on_board instrument7 satellite5)
	(power_avail satellite5)
	(pointing satellite5 phenomenon11)
)
(:goal (and
	(pointing satellite0 star8)
	(pointing satellite1 star4)
	(pointing satellite2 planet9)
	(pointing satellite3 star1)
	(have_image planet5 thermograph0)
	(have_image star6 thermograph2)
	(have_image phenomenon7 thermograph1)
	(have_image star8 infrared3)
	(have_image planet9 thermograph0)
	(have_image star10 thermograph0)
	(have_image phenomenon11 thermograph2)
))

)
