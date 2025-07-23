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
	infrared1 - mode
	image0 - mode
	image2 - mode
	groundstation0 - direction
	groundstation2 - direction
	star1 - direction
	star3 - direction
	planet4 - direction
	planet5 - direction
	phenomenon6 - direction
	phenomenon7 - direction
	phenomenon8 - direction
	star9 - direction
)
(:init
	(supports instrument0 infrared1)
	(supports instrument0 image2)
	(supports instrument0 image0)
	(calibration_target instrument0 groundstation2)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 planet4)
	(supports instrument1 image0)
	(supports instrument1 image2)
	(calibration_target instrument1 star3)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 phenomenon7)
	(supports instrument2 image2)
	(calibration_target instrument2 star1)
	(supports instrument3 image0)
	(supports instrument3 image2)
	(supports instrument3 infrared1)
	(calibration_target instrument3 groundstation2)
	(on_board instrument2 satellite2)
	(on_board instrument3 satellite2)
	(power_avail satellite2)
	(pointing satellite2 phenomenon6)
	(supports instrument4 image2)
	(supports instrument4 image0)
	(calibration_target instrument4 star1)
	(supports instrument5 infrared1)
	(supports instrument5 image2)
	(calibration_target instrument5 star1)
	(on_board instrument4 satellite3)
	(on_board instrument5 satellite3)
	(power_avail satellite3)
	(pointing satellite3 phenomenon8)
	(supports instrument6 image2)
	(supports instrument6 infrared1)
	(calibration_target instrument6 star3)
	(on_board instrument6 satellite4)
	(power_avail satellite4)
	(pointing satellite4 star3)
)
(:goal (and
	(pointing satellite3 star3)
	(have_image planet4 image2)
	(have_image planet5 image2)
	(have_image phenomenon6 infrared1)
	(have_image phenomenon7 infrared1)
	(have_image phenomenon8 infrared1)
	(have_image star9 image0)
))

)
