#include <gflags/gflags.h>


DEFINE_string(
    calculator_graph_config_file, "",
    "Name of file containing text format CalculatorGraphConfig proto.");

DEFINE_string(input_side_packets, "",
              "Comma-separated list of key=value pairs specifying side packets "
              "for the CalculatorGraph. All values will be treated as the "
              "string type even if they represent doubles, floats, etc.");

// Local file output flags.
// Output stream
DEFINE_string(output_stream, "",
              "The output stream to output to the local file in csv format.");
DEFINE_string(output_stream_file, "",
              "The name of the local file to output all packets sent to "
              "the stream specified with --output_stream. ");
DEFINE_bool(strip_timestamps, false,
            "If true, only the packet contents (without timestamps) will be "
            "written into the local file.");
// Output side packets
DEFINE_string(output_side_packets, "",
              "A CSV of output side packets to output to local file.");
DEFINE_string(output_side_packets_file, "",
              "The name of the local file to output all side packets specified "
              "with --output_side_packets. ");


mediapipe::MakePacket<std::string>

get_str(packet)
