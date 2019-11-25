/*
* CS-E4640
* Linh Truong
* Edited by Antoine Louis
*/
package analytics;

import java.io.StringReader;
import java.util.Date;
import java.util.ArrayList;
import java.util.List;
import java.text.SimpleDateFormat;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.CheckpointingMode;
import org.apache.flink.streaming.api.TimeCharacteristic;
import org.apache.flink.api.java.utils.ParameterTool;
import org.apache.flink.types.Row;
import org.apache.flink.api.common.typeinfo.TypeInformation;
import org.apache.flink.streaming.connectors.rabbitmq.common.RMQConnectionConfig;
import org.apache.flink.streaming.connectors.rabbitmq.RMQSource;
import org.apache.flink.streaming.connectors.rabbitmq.RMQSink;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.datastream.KeyedStream;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.streaming.api.windowing.windows.Window;
import org.apache.flink.api.java.tuple.Tuple;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.streaming.api.windowing.assigners.SlidingTimeWindows;
import org.apache.flink.streaming.api.windowing.assigners.SlidingProcessingTimeWindows;
import org.apache.flink.streaming.api.windowing.assigners.SlidingEventTimeWindows;
import org.apache.flink.streaming.api.functions.windowing.WindowFunction;
import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.streaming.api.datastream.SplitStream;
import org.apache.flink.streaming.api.collector.selector.OutputSelector;
import org.apache.flink.util.Collector;
import org.apache.flink.streaming.api.functions.windowing.ProcessWindowFunction;
import org.apache.flink.api.java.functions.KeySelector;
import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVRecord;


public class CustomerStreamApp {

	// Variables
	private static String input_rabbitMQ;
	private static String inputQueue;
	private static String outputQueue;
	private static int parallelismDegree;



	public static void main(String[] args) throws Exception {

		// Parse input parameters
		parse_input_parameters(args);

		// Set up the environment
		final StreamExecutionEnvironment env = setup_environment();

		// Connect data source with RabbitMQ
		final RMQConnectionConfig connectionConfig = new RMQConnectionConfig.Builder()
    			.setHost(input_rabbitMQ)
				.setVirtualHost("/")
				.setUserName("guest")
				.setPassword("guest")
				.setPort(5672)
    			.build();

		// Build schema for the input DataStream
		SimpleStringSchema inputSchema = new SimpleStringSchema();

		// Declare RabbitMQ as a source of data and set parallelism degree
		RMQSource<String> btsdatasource = new RMQSource(
				connectionConfig,            // config for the RabbitMQ connection
				inputQueue,                 // name of the RabbitMQ queue to consume
				false,       // no correlation between event
				inputSchema);
		final DataStream<String> btsdatastream = env
    			.addSource(btsdatasource)   // deserialization schema for input
    			.setParallelism(parallelismDegree);

		// Parse initial datastream
		DataStream<BTSEvent> parsedDataStream = btsdatastream.flatMap(new BTSParser());

		// Filter datastream to handle deseralization errors
		SplitStream<BTSEvent> splitDataStream = parsedDataStream.split(new OutputSelector<BTSEvent>() {
            @Override
            public Iterable<String> select(BTSEvent event) {
                List<String> split = new ArrayList<String>();
                if (event.isDeserialized) {
                    split.add("deserialization_ok");
                }
                else {
                    split.add("deserialization_error");
                }
                return split;
            }
        });
        DataStream<BTSEvent> filteredDataStream = splitDataStream.select("deserialization_ok");
        DataStream<BTSEvent> errorDataStream = splitDataStream.select("deserialization_error");

		// Keye datastream by "station_id-datapoint_id-alarm_id"
		KeyedStream<BTSEvent, String> keyedDataStream = filteredDataStream.keyBy(new StatisticsKeySelector());

		// Process Global Streaming Analytics
		DataStream<String> analyticsGlobalStream = keyedDataStream.process(new GlobalStatisticsFunction());

		// Process Window Streaming Analytics
		DataStream<String> analyticsWindowStream = keyedDataStream
                .window(SlidingProcessingTimeWindows.of(Time.minutes(1), Time.seconds(5)))
                .process(new MyProcessWindowFunction());

		// Send analytics and errors to the output queue of the customer
		RMQSink<String> sink = new RMQSink<String>(
				connectionConfig,
				outputQueue,
				new SimpleStringSchema());
		analyticsGlobalStream.addSink(sink);
		analyticsWindowStream.addSink(sink);
		errorDataStream.flatMap(new BTSToString()).addSink(sink);

		// Print out the result
		analyticsGlobalStream.print().setParallelism(1);
		analyticsWindowStream.print().setParallelism(1);

		// Execute environment
		env.execute("CustomerStreamApp");
	}


	private static void parse_input_parameters(String[] args){
		// Use Flink ParameterTool to parse input parameters
		try {
			final ParameterTool params = ParameterTool.fromArgs(args);
			input_rabbitMQ = params.get("amqpurl");
			inputQueue = params.get("iqueue");
			outputQueue = params.get("oqueue");
			parallelismDegree = params.getInt("parallelism");
		} catch (Exception e) {
			System.err.println("'LowSpeedDetection --amqpurl <rabbitmq url>  --iqueue <input data queue> --oqueue <output data queue> --parallelism <degree of parallelism>'");
		}
	}


	private static StreamExecutionEnvironment setup_environment(){
		// Set up the execution getExecutionEnvironment
		final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

		// Use checkpoint to select level of message guarantees. Here: EXACTLY_ONCE
		final CheckpointingMode checkpointMode = CheckpointingMode.EXACTLY_ONCE;
		env.enableCheckpointing(1000*60, checkpointMode);

		// Define the event time (ProcessingTime or EventTime). NB: if using EventTime, then we need to assignTimestampsAndWatermarks
		env.setStreamTimeCharacteristic(TimeCharacteristic.ProcessingTime);

		return  env;
	}

}
