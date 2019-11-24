package analytics;

import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.util.Collector;


public class BTSToString implements FlatMapFunction<BTSEvent, String> {

    @Override
    public void flatMap(BTSEvent error, Collector<String> out) {
        out.collect(error.showError());
    };
}
