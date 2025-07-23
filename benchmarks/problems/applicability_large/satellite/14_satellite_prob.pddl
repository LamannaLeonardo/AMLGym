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
	instrument5 - instrument
	satellite4 - satellite
	instrument6 - instrument
	instrument7 - instrument
	image1 - mode
	spectrograph0 - mode
	infrared2 - mode
	groundstation2 - direction
	groundstation1 - direction
	star0 - direction
	groundstation3 - direction
	planet4 - direction
	phenomenon5 - direction
	phenomenon6 - direction
	planet7 - direction
	planet8 - direction
	planet9 - direction
)
(:init
	(supports instrument0 infrared2)
	(calibration_target instrument0 groundstation3)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 phenomenon6)
	(supports instrument1 infrared2)
	(calibration_target instrument1 star0)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 groundstation1)
	(supports instrument2 infrared2)
	(supports instrument2 spectrograph0)
	(supports instrument2 image1)
	(calibration_target instrument2 groundstation1)
	(supports instrument3 image1)
	(supports instrument3 infrared2)
	(calibration_target instrument3 groundstation1)
	(on_board instrument2 satellite2)
	(on_board instrument3 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star0)
	(supports instrument4 image1)
	(calibration_target instrument4 groundstation1)
	(supports instrument5 image1)
	(supports instrument5 infrared2)
	(supports instrument5 spectrograph0)
	(calibration_target instrument5 star0)
	(on_board instrument4 satellite3)
	(on_board instrument5 satellite3)
	(power_avail satellite3)
	(pointing satellite3 phenomenon6)
	(supports instrument6 image1)
	(calibration_target instrument6 star0)
	(supports instrument7 infrared2)
	(supports instrument7 image1)
	(supports instrument7 spectrograph0)
	(calibration_target instrument7 groundstation3)
	(on_board instrument6 satellite4)
	(on_board instrument7 satellite4)
	(power_avail satellite4)
	(pointing satellite4 groundstation1)
)
(:goal (and
	(pointing satellite0 phenomenon5)
	(pointing satellite2 planet9)
	(pointing satellite3 groundstation3)
	(have_image planet4 infrared2)
	(have_image phenomenon5 image1)
	(have_image phenomenon6 image1)
	(have_image planet7 spectrograph0)
	(have_image planet8 image1)
	(have_image planet9 image1)
))

)
