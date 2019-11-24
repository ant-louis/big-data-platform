package analytics;

import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.functions.KeyedProcessFunction;
import org.apache.flink.streaming.api.functions.KeyedProcessFunction.Context;
import org.apache.flink.streaming.api.functions.KeyedProcessFunction.OnTimerContext;
import org.apache.flink.util.Collector;


public class MyStatsFunction extends KeyedProcessFunction<String, BTSEvent, String> {

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
        if (input.isActive == True) {
            current.active_counter++;
        }


        // Output
        String key = input.station_id+"-"+input.datapoint_id+"-"+input.alarm_id;
        out.collect("Key: "+key+" . Counter "+Double.toString(current.counter)+" . Active counter: "+Double.toString(current.active_counter));

        // Update the state
        state.update(current);
    }    
}
