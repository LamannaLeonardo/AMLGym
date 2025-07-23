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
	satellite4 - satellite
	instrument5 - instrument
	image1 - mode
	infrared2 - mode
	image3 - mode
	infrared0 - mode
	groundstation0 - direction
	star2 - direction
	groundstation3 - direction
	star1 - direction
	star4 - direction
	star5 - direction
	planet6 - direction
	phenomenon7 - direction
	star8 - direction
	phenomenon9 - direction
)
(:init
	(supports instrument0 infrared2)
	(supports instrument0 infrared0)
	(calibration_target instrument0 star1)
	(supports instrument1 infrared0)
	(calibration_target instrument1 star1)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star1)
	(supports instrument2 image3)
	(supports instrument2 image1)
	(calibration_target instrument2 groundstation3)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star4)
	(supports instrument3 infrared0)
	(supports instrument3 image1)
	(supports instrument3 image3)
	(calibration_target instrument3 groundstation3)
	(on_board instrument3 satellite2)
	(power_avail satellite2)
	(pointing satellite2 groundstation0)
	(supports instrument4 image3)
	(supports instrument4 image1)
	(calibration_target instrument4 groundstation3)
	(on_board instrument4 satellite3)
	(power_avail satellite3)
	(pointing satellite3 star4)
	(supports instrument5 image1)
	(supports instrument5 image3)
	(calibration_target instrument5 star1)
	(on_board instrument5 satellite4)
	(power_avail satellite4)
	(pointing satellite4 phenomenon9)
)
(:goal (and
	(pointing satellite0 phenomenon7)
	(pointing satellite1 planet6)
	(pointing satellite2 star1)
	(have_image star4 infrared2)
	(have_image star5 image3)
	(have_image planet6 infrared2)
	(have_image phenomenon7 image1)
	(have_image star8 image1)
	(have_image phenomenon9 image1)
))

)
