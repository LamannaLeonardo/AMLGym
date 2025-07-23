(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	satellite1 - satellite
	instrument2 - instrument
	satellite2 - satellite
	instrument3 - instrument
	instrument4 - instrument
	satellite3 - satellite
	instrument5 - instrument
	instrument6 - instrument
	satellite4 - satellite
	instrument7 - instrument
	infrared0 - mode
	image1 - mode
	spectrograph2 - mode
	thermograph3 - mode
	groundstation2 - direction
	groundstation0 - direction
	groundstation3 - direction
	star1 - direction
	phenomenon4 - direction
	planet5 - direction
	phenomenon6 - direction
	planet7 - direction
	phenomenon8 - direction
	planet9 - direction
)
(:init
	(supports instrument0 image1)
	(calibration_target instrument0 groundstation2)
	(supports instrument1 infrared0)
	(calibration_target instrument1 groundstation0)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 groundstation2)
	(supports instrument2 spectrograph2)
	(calibration_target instrument2 groundstation2)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star1)
	(supports instrument3 infrared0)
	(calibration_target instrument3 groundstation3)
	(supports instrument4 infrared0)
	(supports instrument4 thermograph3)
	(calibration_target instrument4 groundstation2)
	(on_board instrument3 satellite2)
	(on_board instrument4 satellite2)
	(power_avail satellite2)
	(pointing satellite2 phenomenon8)
	(supports instrument5 thermograph3)
	(supports instrument5 infrared0)
	(calibration_target instrument5 groundstation0)
	(supports instrument6 image1)
	(calibration_target instrument6 groundstation3)
	(on_board instrument5 satellite3)
	(on_board instrument6 satellite3)
	(power_avail satellite3)
	(pointing satellite3 groundstation3)
	(supports instrument7 thermograph3)
	(supports instrument7 spectrograph2)
	(calibration_target instrument7 star1)
	(on_board instrument7 satellite4)
	(power_avail satellite4)
	(pointing satellite4 phenomenon4)
)
(:goal (and
	(pointing satellite1 phenomenon8)
	(pointing satellite3 groundstation2)
	(have_image phenomenon4 infrared0)
	(have_image planet5 infrared0)
	(have_image phenomenon6 infrared0)
	(have_image planet7 infrared0)
	(have_image phenomenon8 infrared0)
	(have_image planet9 infrared0)
))

)
