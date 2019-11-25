package analytics;

import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.functions.KeyedProcessFunction;
import org.apache.flink.streaming.api.functions.KeyedProcessFunction.Context;
import org.apache.flink.streaming.api.functions.KeyedProcessFunction.OnTimerContext;
import org.apache.flink.util.Collector;


public class GlobalStatisticsFunction extends KeyedProcessFunction<String, BTSEvent, String> {

    private ValueState<Statistics> state;

    @Override
    public void open(Configuration parameters) throws Exception {
        state = getRuntimeContext().getState(new ValueStateDescriptor<>("myState", Statistics.class));
    }


    @Override
    public void processElement(BTSEvent input, Context context, Collector<String> out) throws Exception{
        // Access the state value 
        Statistics current = state.value();
        if (current == null) {
            current = new Statistics();
        }

        // Counter of event
        current.counter++;

        // Counter of event where alarm is Active
        if (input.isActive) {
            current.active_counter++;
        }

        // Check the min
        if (input.value < current.min){
            current.min = input.value;
        }

        // Check the max
        if (input.value > current.max){
            current.max = input.value;
        }

        // Compute the mean
        current.sum += input.value;
        current.mean = current.sum / current.counter;

        // Output
        BTSAlert alert = new BTSAlert(
            input.station_id,
            input.datapoint_id,
            input.alarm_id,
            Long.toString(current.counter),
            Long.toString(current.active_counter),
            Double.toString(current.min),
            Double.toString(current.max),
            Double.toString(current.mean)
            );
        out.collect(alert.statMessage());

        // Update the state
        state.update(current);
    }    
}
