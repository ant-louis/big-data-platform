package analytics;

import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.util.Collector;


public class BTSToString implements FlatMapFunction<BTSEvent, String> {

    @Override
    public void flatMap(BTSEvent errorEvent, Collector<String> out) {
        // Remove the newline char
        String message = errorEvent.error.replaceAll("\n", "");

        // Create an alert
        out.collect(new BTSAlert(message).errorMessage());
    };
}
