package analytics;

import org.apache.flink.streaming.api.functions.windowing.ProcessWindowFunction;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.util.Collector;


public class NewFunction extends ProcessWindowFunction<BTSAlarmEvent, String, String, TimeWindow> {
    // Simple function to detect a sequence of alarms in a round
    @Override
    public void process(String station_id, Context context, Iterable<BTSAlarmEvent> records, Collector<String> out) {
        out.collect (new BTSAlarmAlert(station_id,true).toJSON());

    }
}
