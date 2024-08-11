import photonlibpy.photonPoseEstimator
import photonlibpy.photonCamera
from robotpy_apriltag import AprilTagField

import config


class ApriltagHandler:
   def __init__(self):
      self.field = photonlibpy.photonPoseEstimator.AprilTagFieldLayout().loadField(AprilTagField.k2024Crescendo)
      self.camera = photonlibpy.photonCamera.PhotonCamera("camera1")
      self.poseEstimator = photonlibpy.photonPoseEstimator.PhotonPoseEstimator(
         self.field,
         photonlibpy.photonPoseEstimator.PoseStrategy.MULTI_TAG_PNP_ON_COPROCESSOR,
         self.camera,
         config.camera1Pose
      )

   def getPose(self):
      pose = self.poseEstimator.update(self.camera.getLatestResult())
      return pose.estimatedPose



