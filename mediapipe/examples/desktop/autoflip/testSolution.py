hand_tracker = solution_base.SolutionBase(
    binary_graph_path='mediapipe/modules/hand_landmark/hand_landmark_tracking_cpu.binarypb',
    side_inputs={'num_hands': 2})
# Read an image and convert the BGR image to RGB.
input_image = cv2.cvtColor(cv2.imread('/tmp/hand.png'), COLOR_BGR2RGB)
results = hand_tracker.process(input_image)
print(results.palm_detections)
print(results.multi_hand_landmarks)
hand_tracker.close()