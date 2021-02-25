import mediapipe as mp
import cv2
import collections

config_text = """
  input_stream: 'in_stream'
  output_stream: 'out_stream'
  node {
    calculator: 'PassThroughCalculator'
    input_stream: 'in_stream'
    output_stream: 'out_stream'
  }
"""
graph = mp.CalculatorGraph(graph_config=config_text)
output_packets = []
graph.observe_output_stream(
    'out_stream',
    lambda stream_name, packet:
        output_packets.append(mp.packet_getter.get_str(packet)))

graph.start_run()

graph.add_packet_to_input_stream(
    'in_stream', mp.packet_creator.create_string('abc').at(0))

#rgb_img = cv2.cvtColor(cv2.imread('car.png'), cv2.COLOR_BGR2RGB)
#graph.add_packet_to_input_stream(
#    'in_stream',
#    mp.packet_creator.create_image_frame(image_format=mp.ImageFormat.SRGB,
#                                         data=rgb_img).at(1))
graph.wait_until_idle()
solution_outputs = collections.namedtuple(
    'SolutionOutputs', self._output_stream_type_info.keys())
for stream_name in self._output_stream_type_info.keys():
  if stream_name in self._graph_outputs:
    setattr(
        solution_outputs, stream_name,
        self._get_packet_content(self._output_stream_type_info[stream_name],
                                  self._graph_outputs[stream_name]))
  else:
    setattr(solution_outputs, stream_name, None)

graph.close()