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
	satellite3 - satellite
	instrument4 - instrument
	instrument5 - instrument
	satellite4 - satellite
	instrument6 - instrument
	instrument7 - instrument
	image3 - mode
	image0 - mode
	spectrograph1 - mode
	infrared2 - mode
	star1 - direction
	groundstation2 - direction
	groundstation0 - direction
	groundstation3 - direction
	planet4 - direction
	star5 - direction
	phenomenon6 - direction
	planet7 - direction
	phenomenon8 - direction
	planet9 - direction
)
(:init
	(supports instrument0 image3)
	(calibration_target instrument0 groundstation0)
	(supports instrument1 infrared2)
	(supports instrument1 image3)
	(supports instrument1 image0)
	(calibration_target instrument1 groundstation3)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 planet4)
	(supports instrument2 image3)
	(calibration_target instrument2 groundstation3)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 groundstation0)
	(supports instrument3 infrared2)
	(supports instrument3 image3)
	(supports instrument3 image0)
	(calibration_target instrument3 groundstation3)
	(on_board instrument3 satellite2)
	(power_avail satellite2)
	(pointing satellite2 planet9)
	(supports instrument4 spectrograph1)
	(supports instrument4 image0)
	(calibration_target instrument4 groundstation2)
	(supports instrument5 infrared2)
	(supports instrument5 image0)
	(supports instrument5 spectrograph1)
	(calibration_target instrument5 groundstation0)
	(on_board instrument4 satellite3)
	(on_board instrument5 satellite3)
	(power_avail satellite3)
	(pointing satellite3 groundstation0)
	(supports instrument6 image0)
	(supports instrument6 infrared2)
	(calibration_target instrument6 groundstation0)
	(supports instrument7 image0)
	(supports instrument7 infrared2)
	(supports instrument7 spectrograph1)
	(calibration_target instrument7 groundstation3)
	(on_board instrument6 satellite4)
	(on_board instrument7 satellite4)
	(power_avail satellite4)
	(pointing satellite4 groundstation0)
)
(:goal (and
	(have_image planet4 image0)
	(have_image star5 image0)
	(have_image phenomenon6 image3)
	(have_image planet7 infrared2)
	(have_image phenomenon8 image0)
	(have_image planet9 image3)
))

)
