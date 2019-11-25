package analytics;

import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.util.Collector;


public class BTSError implements FlatMapFunction<BTSEvent, String> {

    public long nbErrors = 0;

    @Override
    public void flatMap(BTSEvent errorEvent, Collector<String> out) {
        // Remove the newline char
        String message = errorEvent.errorLine.replaceAll("\n", "");

        // Increment number of errors
        nbErrors++;

        // Create an alert
        out.collect(new BTSAlert(message, Long.toString(nbErrors)).errorMessage());
    };
}
