load("//mediapipe/framework/port:build_config.bzl", "mediapipe_cc_proto_library")
load("//mediapipe/framework/tool:mediapipe_graph.bzl", "mediapipe_simple_subgraph")

# Copyright 2019 The MediaPipe Authors.
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

licenses(["notice"])

package(default_visibility = ["//visibility:public"])

proto_library(
    name = "autoflip_messages_proto",
    srcs = ["autoflip_messages.proto"],
    deps = [
        "//mediapipe/framework:calculator_proto",
    ],
)

mediapipe_cc_proto_library(
    name = "autoflip_messages_cc_proto",
    srcs = ["autoflip_messages.proto"],
    cc_deps = ["//mediapipe/framework:calculator_cc_proto"],
    visibility = [
        "//visibility:public",
    ],
    deps = [":autoflip_messages_proto"],
)


mediapipe_simple_subgraph(
    name = "autoflip_cpu",
    graph = "autoflip_graph.pbtxt",
    register_as = "AutoFlipCpu",
    deps = [
        "//mediapipe/calculators/core:packet_thinner_calculator",
        "//mediapipe/calculators/image:scale_image_calculator",
        "//mediapipe/calculators/video:opencv_video_decoder_calculator",
        "//mediapipe/calculators/video:opencv_video_encoder_calculator",
        "//mediapipe/calculators/video:video_pre_stream_calculator",
        "//mediapipe/examples/desktop:simple_run_graph_main",
        "//mediapipe/modules/autoflip/calculators:border_detection_calculator",
        "//mediapipe/modules/autoflip/calculators:face_to_region_calculator",
        "//mediapipe/modules/autoflip/calculators:localization_to_region_calculator",
        "//mediapipe/modules/autoflip/calculators:scene_cropping_calculator",
        "//mediapipe/modules/autoflip/calculators:shot_boundary_calculator",
        "//mediapipe/modules/autoflip/calculators:signal_fusing_calculator",
        "//mediapipe/modules/autoflip/calculators:video_filtering_calculator",
        "//mediapipe/modules/autoflip/subgraph:autoflip_face_detection_subgraph",
        "//mediapipe/modules/autoflip/subgraph:autoflip_object_detection_subgraph",
    ],
)

cc_binary(
    name = "run_autoflip",
    deps = [
        "//mediapipe/calculators/core:packet_thinner_calculator",
        "//mediapipe/calculators/image:scale_image_calculator",
        "//mediapipe/calculators/video:opencv_video_decoder_calculator",
        "//mediapipe/calculators/video:opencv_video_encoder_calculator",
        "//mediapipe/calculators/video:video_pre_stream_calculator",
        "//mediapipe/examples/desktop:simple_run_graph_main",
        "//mediapipe/modules/autoflip/calculators:border_detection_calculator",
        "//mediapipe/modules/autoflip/calculators:face_to_region_calculator",
        "//mediapipe/modules/autoflip/calculators:localization_to_region_calculator",
        "//mediapipe/modules/autoflip/calculators:scene_cropping_calculator",
        "//mediapipe/modules/autoflip/calculators:shot_boundary_calculator",
        "//mediapipe/modules/autoflip/calculators:signal_fusing_calculator",
        "//mediapipe/modules/autoflip/calculators:video_filtering_calculator",
        "//mediapipe/modules/autoflip/subgraph:autoflip_face_detection_subgraph",
        "//mediapipe/modules/autoflip/subgraph:autoflip_object_detection_subgraph",
    ],
)
