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
	satellite5 - satellite
	instrument6 - instrument
	instrument7 - instrument
	infrared3 - mode
	image2 - mode
	thermograph1 - mode
	infrared0 - mode
	star2 - direction
	groundstation4 - direction
	groundstation1 - direction
	star3 - direction
	groundstation0 - direction
	star5 - direction
	planet6 - direction
	star7 - direction
	star8 - direction
	phenomenon9 - direction
	phenomenon10 - direction
	planet11 - direction
)
(:init
	(supports instrument0 infrared3)
	(supports instrument0 thermograph1)
	(calibration_target instrument0 star3)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star7)
	(supports instrument1 infrared0)
	(supports instrument1 image2)
	(calibration_target instrument1 groundstation0)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 planet11)
	(supports instrument2 infrared3)
	(supports instrument2 thermograph1)
	(supports instrument2 infrared0)
	(calibration_target instrument2 star3)
	(supports instrument3 image2)
	(supports instrument3 thermograph1)
	(calibration_target instrument3 groundstation0)
	(on_board instrument2 satellite2)
	(on_board instrument3 satellite2)
	(power_avail satellite2)
	(pointing satellite2 phenomenon10)
	(supports instrument4 image2)
	(supports instrument4 infrared0)
	(supports instrument4 thermograph1)
	(calibration_target instrument4 groundstation0)
	(on_board instrument4 satellite3)
	(power_avail satellite3)
	(pointing satellite3 phenomenon10)
	(supports instrument5 infrared0)
	(supports instrument5 infrared3)
	(calibration_target instrument5 groundstation1)
	(on_board instrument5 satellite4)
	(power_avail satellite4)
	(pointing satellite4 phenomenon9)
	(supports instrument6 infrared3)
	(supports instrument6 thermograph1)
	(calibration_target instrument6 star3)
	(supports instrument7 image2)
	(supports instrument7 infrared3)
	(calibration_target instrument7 groundstation0)
	(on_board instrument6 satellite5)
	(on_board instrument7 satellite5)
	(power_avail satellite5)
	(pointing satellite5 planet11)
)
(:goal (and
	(pointing satellite0 star3)
	(have_image star5 infrared3)
	(have_image planet6 infrared3)
	(have_image star7 thermograph1)
	(have_image star8 image2)
	(have_image phenomenon9 infrared3)
	(have_image phenomenon10 thermograph1)
	(have_image planet11 infrared3)
))

)
