(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	satellite2 - satellite
	instrument2 - instrument
	instrument3 - instrument
	satellite3 - satellite
	instrument4 - instrument
	satellite4 - satellite
	instrument5 - instrument
	instrument6 - instrument
	satellite5 - satellite
	instrument7 - instrument
	thermograph0 - mode
	thermograph3 - mode
	image2 - mode
	infrared1 - mode
	star0 - direction
	groundstation4 - direction
	groundstation3 - direction
	groundstation2 - direction
	groundstation1 - direction
	phenomenon5 - direction
	phenomenon6 - direction
	phenomenon7 - direction
	phenomenon8 - direction
	planet9 - direction
	phenomenon10 - direction
	star11 - direction
)
(:init
	(supports instrument0 image2)
	(calibration_target instrument0 groundstation4)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 groundstation3)
	(supports instrument1 infrared1)
	(supports instrument1 thermograph0)
	(supports instrument1 image2)
	(calibration_target instrument1 groundstation3)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 groundstation2)
	(supports instrument2 image2)
	(supports instrument2 thermograph3)
	(calibration_target instrument2 groundstation4)
	(supports instrument3 thermograph0)
	(supports instrument3 infrared1)
	(supports instrument3 thermograph3)
	(calibration_target instrument3 groundstation3)
	(on_board instrument2 satellite2)
	(on_board instrument3 satellite2)
	(power_avail satellite2)
	(pointing satellite2 groundstation1)
	(supports instrument4 thermograph0)
	(supports instrument4 image2)
	(supports instrument4 infrared1)
	(calibration_target instrument4 groundstation2)
	(on_board instrument4 satellite3)
	(power_avail satellite3)
	(pointing satellite3 groundstation2)
	(supports instrument5 thermograph3)
	(calibration_target instrument5 groundstation2)
	(supports instrument6 image2)
	(calibration_target instrument6 groundstation2)
	(on_board instrument5 satellite4)
	(on_board instrument6 satellite4)
	(power_avail satellite4)
	(pointing satellite4 phenomenon7)
	(supports instrument7 thermograph0)
	(supports instrument7 thermograph3)
	(calibration_target instrument7 groundstation1)
	(on_board instrument7 satellite5)
	(power_avail satellite5)
	(pointing satellite5 phenomenon8)
)
(:goal (and
	(pointing satellite3 groundstation3)
	(have_image phenomenon5 infrared1)
	(have_image phenomenon6 image2)
	(have_image phenomenon7 thermograph3)
	(have_image phenomenon8 image2)
	(have_image planet9 image2)
	(have_image phenomenon10 thermograph0)
	(have_image star11 thermograph0)
))

)
