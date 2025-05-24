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
	thermograph0 - mode
	infrared1 - mode
	spectrograph2 - mode
	star3 - direction
	star1 - direction
	groundstation2 - direction
	groundstation0 - direction
	planet4 - direction
	planet5 - direction
	phenomenon6 - direction
	planet7 - direction
	star8 - direction
	phenomenon9 - direction
)
(:init
	(supports instrument0 thermograph0)
	(supports instrument0 infrared1)
	(supports instrument0 spectrograph2)
	(calibration_target instrument0 star3)
	(supports instrument1 thermograph0)
	(calibration_target instrument1 star1)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star8)
	(supports instrument2 thermograph0)
	(supports instrument2 spectrograph2)
	(calibration_target instrument2 groundstation2)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 planet7)
	(supports instrument3 thermograph0)
	(supports instrument3 infrared1)
	(calibration_target instrument3 groundstation2)
	(on_board instrument3 satellite2)
	(power_avail satellite2)
	(pointing satellite2 planet7)
	(supports instrument4 spectrograph2)
	(calibration_target instrument4 groundstation2)
	(on_board instrument4 satellite3)
	(power_avail satellite3)
	(pointing satellite3 star1)
	(supports instrument5 thermograph0)
	(supports instrument5 spectrograph2)
	(calibration_target instrument5 groundstation0)
	(on_board instrument5 satellite4)
	(power_avail satellite4)
	(pointing satellite4 star8)
)
(:goal (and
	(pointing satellite4 planet7)
	(have_image planet4 thermograph0)
	(have_image planet5 spectrograph2)
	(have_image phenomenon6 thermograph0)
	(have_image planet7 infrared1)
	(have_image star8 spectrograph2)
	(have_image phenomenon9 thermograph0)
))

)
