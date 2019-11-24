package analytics;

import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.streaming.api.functions.KeyedProcessFunction;
import org.apache.flink.util.Collector;
import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.api.common.typeinfo.TypeHint;
import org.apache.flink.api.common.typeinfo.Types;
import org.apache.flink.api.common.typeinfo.TypeInformation;


public class StatisticsFunction extends KeyedProcessFunction<String, BTSEvent, String> {

    private transient ValueState<Tuple2<Long, Float>> sum;


    // Simple function to detect a sequence of alarms in a round
    @Override
    public void processElement(BTSEvent input, Context context, Collector<String> out) throws Exception{
        // Access the state value
        Tuple2<Long, Float> currentSum = sum.value();

        // Update the count and add the second field of the input value
        currentSum.f0 += 1;
        currentSum.f1 += input.value;

        // Output
        out.collect("Counter: "+Long.toString(currentSum.f0)+" with current sum of "+Float.toString(currentSum.f1));

        // Update the state
        sum.update(currentSum);

        // if the count reaches 5, emit the average and clear the state
        if (currentSum.f0 >= 5) {
            float mean = currentSum.f1 / currentSum.f0;
            out.collect("Counter: "+ Long.toString(currentSum.f0) + ". Mean: " + Float.toString(mean));
            sum.clear();
        }
    }

    @Override
    public void open(Configuration config) {
        ValueStateDescriptor<Tuple2<Long, Float>> descriptor =
                new ValueStateDescriptor(
                        "average", // the state name
                        TypeInformation.of(new TypeHint<Tuple2<Long, Float>>() {}), // type information
                        Tuple2.of(0L, 0.0f)); // default value of the state, if nothing was set
        sum = getRuntimeContext().getState(descriptor);
    }



}
