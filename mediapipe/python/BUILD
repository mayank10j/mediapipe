# Copyright 2020 The MediaPipe Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

load("@pybind11_bazel//:build_defs.bzl", "pybind_extension")

licenses(["notice"])  # Apache 2.0

pybind_extension(
    name = "_framework_bindings",
    srcs = ["framework_bindings.cc"],
    linkopts = select({
        "//third_party:opencv_source_build": [],
        "//conditions:default": [
            "-lopencv_core",
            "-lopencv_imgproc",
            "-lopencv_highgui",
            "-lopencv_video",
            "-lopencv_features2d",
            "-lopencv_calib3d",
            "-lopencv_imgcodecs",
        ],
    }),
    deps = [
        ":builtin_calculators",
        "//mediapipe/python/pybind:calculator_graph",
        "//mediapipe/python/pybind:image_frame",
        "//mediapipe/python/pybind:matrix",
        "//mediapipe/python/pybind:packet",
        "//mediapipe/python/pybind:packet_creator",
        "//mediapipe/python/pybind:packet_getter",
        "//mediapipe/python/pybind:resource_util",
        "//mediapipe/python/pybind:timestamp",
        "//mediapipe/python/pybind:validated_graph_config",
        # Type registration.
        "//mediapipe/framework:basic_types_registration",
        "//mediapipe/framework/formats:classification_registration",
        "//mediapipe/framework/formats:detection_registration",
        "//mediapipe/framework/formats:landmark_registration",
        "//mediapipe/framework/formats:image_format_registration",

    ],
)


cc_library(
    name = "builtin_calculators",
    deps = [
        "//mediapipe/calculators/core:gate_calculator",
        "//mediapipe/calculators/core:pass_through_calculator",
        "//mediapipe/calculators/core:side_packet_to_stream_calculator",
        "//mediapipe/calculators/core:split_normalized_landmark_list_calculator",
        "//mediapipe/calculators/core:string_to_int_calculator",
        "//mediapipe/calculators/core:packet_thinner_calculator",
        "//mediapipe/calculators/image:image_transformation_calculator",
        "//mediapipe/calculators/image:scale_image_calculator",
        "//mediapipe/calculators/video:opencv_video_decoder_calculator",
        "//mediapipe/calculators/video:opencv_video_encoder_calculator",        
        "//mediapipe/calculators/video:video_pre_stream_calculator",
        "//mediapipe/calculators/util:detection_unique_id_calculator",
        "//mediapipe/modules/face_detection:face_detection_front_cpu",
        "//mediapipe/modules/face_landmark:face_landmark_front_cpu",
        "//mediapipe/modules/hand_landmark:hand_landmark_tracking_cpu",
        "//mediapipe/modules/holistic_landmark:holistic_landmark_cpu",
        "//mediapipe/modules/palm_detection:palm_detection_cpu",
        "//mediapipe/modules/pose_detection:pose_detection_cpu",
        "//mediapipe/modules/pose_landmark:pose_landmark_by_roi_cpu",
        "//mediapipe/modules/pose_landmark:pose_landmark_cpu",
        "//mediapipe/modules/autoflip:autoflip_cpu",
        "//mediapipe/modules/autoflip/calculators:border_detection_calculator",
        "//mediapipe/modules/autoflip/calculators:content_zooming_calculator",
        "//mediapipe/modules/autoflip/calculators:face_to_region_calculator",
        "//mediapipe/modules/autoflip/calculators:localization_to_region_calculator",
        "//mediapipe/modules/autoflip/calculators:scene_cropping_calculator",
        "//mediapipe/modules/autoflip/calculators:shot_boundary_calculator",
        "//mediapipe/modules/autoflip/calculators:signal_fusing_calculator",
        "//mediapipe/modules/autoflip/calculators:video_filtering_calculator",
        "//mediapipe/modules/autoflip/subgraph:autoflip_face_detection_subgraph",
        "//mediapipe/modules/autoflip/subgraph:autoflip_object_detection_subgraph",
        "//mediapipe/framework/formats:image_frame_opencv",
        "//mediapipe/framework/formats:image_frame",
        "//mediapipe/framework/formats:matrix",

        #"//mediapipe/modules/autoflip/subgraph:autoflip_face_detection_subgraph",
    ],
)
