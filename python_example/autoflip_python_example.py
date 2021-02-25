import mediapipe as mp
import os


config_text = """
# Autoflip graph that only renders the final cropped video. For use with
# end user applications.
max_queue_size: -1

# VIDEO_PREP: Decodes an input video file into images and a video header.
node {
  calculator: "OpenCvVideoDecoderCalculator"
  input_side_packet: "INPUT_FILE_PATH:input_video_path"
  output_stream: "VIDEO:video_raw"
  output_stream: "VIDEO_PRESTREAM:video_header"
  output_side_packet: "SAVED_AUDIO_PATH:audio_path"
}

# VIDEO_PREP: Scale the input video before feature extraction.
node {
  calculator: "ScaleImageCalculator"
  input_stream: "FRAMES:video_raw"
  input_stream: "VIDEO_HEADER:video_header"
  output_stream: "FRAMES:video_frames_scaled"
  options: {
    [mediapipe.ScaleImageCalculatorOptions.ext]: {
      preserve_aspect_ratio: true
      output_format: SRGB
      target_width: 480
      algorithm: DEFAULT_WITHOUT_UPSCALE
    }
  }
}

# VIDEO_PREP: Create a low frame rate stream for feature extraction.
node {
  calculator: "PacketThinnerCalculator"
  input_stream: "video_frames_scaled"
  output_stream: "video_frames_scaled_downsampled"
  options: {
    [mediapipe.PacketThinnerCalculatorOptions.ext]: {
      thinner_type: ASYNC
      period: 200000
    }
  }
}

# DETECTION: find borders around the video and major background color.
node {
  calculator: "BorderDetectionCalculator"
  input_stream: "VIDEO:video_raw"
  output_stream: "DETECTED_BORDERS:borders"
}

# DETECTION: find shot/scene boundaries on the full frame rate stream.
node {
  calculator: "ShotBoundaryCalculator"
  input_stream: "VIDEO:video_frames_scaled"
  output_stream: "IS_SHOT_CHANGE:shot_change"
  options {
    [mediapipe.autoflip.ShotBoundaryCalculatorOptions.ext] {
      min_shot_span: 0.2
      min_motion: 0.3
      window_size: 15
      min_shot_measure: 10
      min_motion_with_shot_measure: 0.05
    }
  }
}

# DETECTION: find faces on the down sampled stream
node {
  calculator: "AutoFlipFaceDetectionSubgraph"
  input_stream: "VIDEO:video_frames_scaled_downsampled"
  output_stream: "DETECTIONS:face_detections"
}
node {
  calculator: "FaceToRegionCalculator"
  input_stream: "VIDEO:video_frames_scaled_downsampled"
  input_stream: "FACES:face_detections"
  output_stream: "REGIONS:face_regions"
}

# DETECTION: find objects on the down sampled stream
node {
  calculator: "AutoFlipObjectDetectionSubgraph"
  input_stream: "VIDEO:video_frames_scaled_downsampled"
  output_stream: "DETECTIONS:object_detections"
}
node {
  calculator: "LocalizationToRegionCalculator"
  input_stream: "DETECTIONS:object_detections"
  output_stream: "REGIONS:object_regions"
  options {
    [mediapipe.autoflip.LocalizationToRegionCalculatorOptions.ext] {
      output_all_signals: true
    }
  }
}

# SIGNAL FUSION: Combine detections (with weights) on each frame
node {
  calculator: "SignalFusingCalculator"
  input_stream: "shot_change"
  input_stream: "face_regions"
  input_stream: "object_regions"
  output_stream: "salient_regions"
  options {
    [mediapipe.autoflip.SignalFusingCalculatorOptions.ext] {
      signal_settings {
        type { standard: FACE_CORE_LANDMARKS }
        min_score: 0.85
        max_score: 0.9
        is_required: false
      }
      signal_settings {
        type { standard: FACE_ALL_LANDMARKS }
        min_score: 0.8
        max_score: 0.85
        is_required: false
      }
      signal_settings {
        type { standard: FACE_FULL }
        min_score: 0.8
        max_score: 0.85
        is_required: false
      }
      signal_settings {
        type: { standard: HUMAN }
        min_score: 0.75
        max_score: 0.8
        is_required: false
      }
      signal_settings {
        type: { standard: PET }
        min_score: 0.7
        max_score: 0.75
        is_required: false
      }
      signal_settings {
        type: { standard: CAR }
        min_score: 0.7
        max_score: 0.75
        is_required: false
      }
      signal_settings {
        type: { standard: OBJECT }
        min_score: 0.1
        max_score: 0.2
        is_required: false
      }
    }
  }
}

# CROPPING: make decisions about how to crop each frame.
node {
  calculator: "SceneCroppingCalculator"
  input_side_packet: "EXTERNAL_ASPECT_RATIO:aspect_ratio"
  input_stream: "VIDEO_FRAMES:video_raw"
  input_stream: "KEY_FRAMES:video_frames_scaled_downsampled"
  input_stream: "DETECTION_FEATURES:salient_regions"
  input_stream: "STATIC_FEATURES:borders"
  input_stream: "SHOT_BOUNDARIES:shot_change"
  output_stream: "CROPPED_FRAMES:cropped_frames"
  options: {
    [mediapipe.autoflip.SceneCroppingCalculatorOptions.ext]: {
      max_scene_size: 600
      key_frame_crop_options: {
        score_aggregation_type: CONSTANT
      }
      scene_camera_motion_analyzer_options: {
        motion_stabilization_threshold_percent: 0.5
        salient_point_bound: 0.499
      }
      padding_parameters: {
        blur_cv_size: 200
        overlay_opacity: 0.6
      }
      target_size_type: MAXIMIZE_TARGET_DIMENSION
    }
  }
}

# ENCODING(required): encode the video stream for the final cropped output.
node {
  calculator: "VideoPreStreamCalculator"
  # Fetch frame format and dimension from input frames.
  input_stream: "FRAME:cropped_frames"
  # Copying frame rate and duration from original video.
  input_stream: "VIDEO_PRESTREAM:video_header"
  output_stream: "output_frames_video_header"
}

node {
  calculator: "OpenCvVideoEncoderCalculator"
  input_stream: "VIDEO:cropped_frames"
  input_stream: "VIDEO_PRESTREAM:output_frames_video_header"
  input_side_packet: "OUTPUT_FILE_PATH:output_video_path"
  input_side_packet: "AUDIO_FILE_PATH:audio_path"
  options: {
    [mediapipe.OpenCvVideoEncoderCalculatorOptions.ext]: {
      codec: "avc1"
      video_format: "mp4"
    }
  }
}

"""
output_packets = []

input_file_name = "test.mp4"
output_file_name = "test_trimmed.mp4"
target_aspect_ratio = "1:1"
if not os.path.isfile(input_file_name):
  print("Error: FileNotFound Input file: ", input_file_name)
  exit(-1)

if os.path.isfile(output_file_name):
  print("Error: Output file already exist : ", output_file_name)
  exit(-1)

graph = mp.CalculatorGraph(graph_config=config_text)
graph.start_run(
    input_side_packets={
        'input_video_path':
            mp.packet_creator.create_string(input_file_name)
                ,
        'output_video_path':
            mp.packet_creator.create_string(output_file_name)
                ,
        'aspect_ratio':
            mp.packet_creator.create_string(target_aspect_ratio)
                
                
    })

graph.wait_until_done()
graph.close()