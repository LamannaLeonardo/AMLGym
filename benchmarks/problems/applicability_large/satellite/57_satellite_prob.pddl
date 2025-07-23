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
	satellite5 - satellite
	instrument5 - instrument
	instrument6 - instrument
	image0 - mode
	spectrograph4 - mode
	infrared1 - mode
	thermograph2 - mode
	image3 - mode
	groundstation1 - direction
	star3 - direction
	star2 - direction
	groundstation4 - direction
	groundstation0 - direction
	planet5 - direction
	phenomenon6 - direction
	star7 - direction
	planet8 - direction
	planet9 - direction
	phenomenon10 - direction
	phenomenon11 - direction
)
(:init
	(supports instrument0 infrared1)
	(supports instrument0 image3)
	(supports instrument0 image0)
	(calibration_target instrument0 groundstation0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 groundstation4)
	(supports instrument1 spectrograph4)
	(supports instrument1 infrared1)
	(calibration_target instrument1 star2)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 groundstation4)
	(supports instrument2 spectrograph4)
	(calibration_target instrument2 groundstation0)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 planet8)
	(supports instrument3 image0)
	(calibration_target instrument3 star3)
	(on_board instrument3 satellite3)
	(power_avail satellite3)
	(pointing satellite3 planet5)
	(supports instrument4 image3)
	(supports instrument4 image0)
	(supports instrument4 infrared1)
	(calibration_target instrument4 star2)
	(on_board instrument4 satellite4)
	(power_avail satellite4)
	(pointing satellite4 phenomenon10)
	(supports instrument5 infrared1)
	(supports instrument5 thermograph2)
	(supports instrument5 image0)
	(calibration_target instrument5 groundstation4)
	(supports instrument6 image0)
	(supports instrument6 spectrograph4)
	(calibration_target instrument6 groundstation0)
	(on_board instrument5 satellite5)
	(on_board instrument6 satellite5)
	(power_avail satellite5)
	(pointing satellite5 groundstation4)
)
(:goal (and
	(pointing satellite0 planet8)
	(pointing satellite1 star7)
	(pointing satellite3 phenomenon11)
	(have_image planet5 spectrograph4)
	(have_image phenomenon6 image0)
	(have_image star7 image3)
	(have_image planet8 infrared1)
	(have_image planet9 image3)
	(have_image phenomenon10 thermograph2)
	(have_image phenomenon11 spectrograph4)
))

)
