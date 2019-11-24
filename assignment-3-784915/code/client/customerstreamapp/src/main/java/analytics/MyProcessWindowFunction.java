package analytics;

import org.apache.flink.streaming.api.functions.windowing.ProcessWindowFunction;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.util.Collector;


public class MyProcessWindowFunction extends ProcessWindowFunction<BTSEvent, String, String, TimeWindow> {
    
    // Define a simple analytics is that in a windows if an alarm happens N times (true) then we should send an alert.
    @Override
    public void process(String key, Context context, Iterable<BTSEvent> records, Collector<String> out) {
        
        // Variables
        int number_active_threshold = 5; //for study purpose
        int count = 0;

        for (BTSEvent btsrecord: records) {
            if (btsrecord.isActive) {
                count++;
            }   
        }
        if (count > number_active_threshold) {
            out.collect (new BTSAlert(key).alarmMessage());
        }
    }
}
