package analytics;

import org.apache.flink.streaming.api.functions.windowing.ProcessWindowFunction;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.util.Collector;


public class MyProcessWindowFunction extends ProcessWindowFunction<BTSEvent, String, String, TimeWindow> {
    
    // Define a simple analytics is that in a windows if an alarm happens N times (true) then we should send an alert.
    @Override
    public void process(String key, Context context, Iterable<BTSEvent> records, Collector<String> out) {
        
        // Variables
        int number_active_threshold = 5;
        int count = 0;

        // Split the key to get the different ids
        String[] splits = key.split("-");
        String station_id = splits[0];
        String datapoint_id = splits[1];
        String alarm_id = splits[2];

        // Count
        for (BTSEvent btsrecord: records) {
            if (btsrecord.isActive) {
                count++;
            }   
        }

        // If exceed threshold, trigger alert
        if (count > number_active_threshold) {
            out.collect(new BTSAlert(station_id, datapoint_id, alarm_id).alarmMessage());
        }
    }
}
