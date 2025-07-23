(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	instrument2 - instrument
	satellite2 - satellite
	instrument3 - instrument
	instrument4 - instrument
	satellite3 - satellite
	instrument5 - instrument
	instrument6 - instrument
	satellite4 - satellite
	instrument7 - instrument
	instrument8 - instrument
	satellite5 - satellite
	instrument9 - instrument
	thermograph2 - mode
	image0 - mode
	infrared3 - mode
	infrared1 - mode
	star1 - direction
	groundstation0 - direction
	groundstation3 - direction
	groundstation2 - direction
	groundstation4 - direction
	star5 - direction
	star6 - direction
	phenomenon7 - direction
	planet8 - direction
	star9 - direction
	planet10 - direction
	planet11 - direction
)
(:init
	(supports instrument0 infrared3)
	(supports instrument0 image0)
	(calibration_target instrument0 groundstation2)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 phenomenon7)
	(supports instrument1 infrared1)
	(supports instrument1 infrared3)
	(supports instrument1 image0)
	(calibration_target instrument1 star1)
	(supports instrument2 image0)
	(supports instrument2 infrared3)
	(calibration_target instrument2 groundstation0)
	(on_board instrument1 satellite1)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star9)
	(supports instrument3 image0)
	(supports instrument3 thermograph2)
	(calibration_target instrument3 groundstation4)
	(supports instrument4 infrared3)
	(supports instrument4 thermograph2)
	(calibration_target instrument4 groundstation3)
	(on_board instrument3 satellite2)
	(on_board instrument4 satellite2)
	(power_avail satellite2)
	(pointing satellite2 planet8)
	(supports instrument5 infrared1)
	(supports instrument5 thermograph2)
	(supports instrument5 infrared3)
	(calibration_target instrument5 groundstation3)
	(supports instrument6 image0)
	(supports instrument6 infrared3)
	(calibration_target instrument6 groundstation4)
	(on_board instrument5 satellite3)
	(on_board instrument6 satellite3)
	(power_avail satellite3)
	(pointing satellite3 star5)
	(supports instrument7 image0)
	(calibration_target instrument7 groundstation3)
	(supports instrument8 image0)
	(supports instrument8 thermograph2)
	(supports instrument8 infrared1)
	(calibration_target instrument8 groundstation2)
	(on_board instrument7 satellite4)
	(on_board instrument8 satellite4)
	(power_avail satellite4)
	(pointing satellite4 groundstation4)
	(supports instrument9 infrared3)
	(supports instrument9 thermograph2)
	(calibration_target instrument9 groundstation4)
	(on_board instrument9 satellite5)
	(power_avail satellite5)
	(pointing satellite5 planet8)
)
(:goal (and
	(pointing satellite3 groundstation0)
	(have_image star5 infrared3)
	(have_image star6 image0)
	(have_image phenomenon7 infrared1)
	(have_image planet8 thermograph2)
	(have_image star9 image0)
	(have_image planet10 infrared3)
	(have_image planet11 image0)
))

)
