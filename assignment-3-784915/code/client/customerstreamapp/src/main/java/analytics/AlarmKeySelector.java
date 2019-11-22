package analytics;

import org.apache.flink.api.java.functions.KeySelector;


public class AlarmKeySelector implements KeySelector<BTSAlarmEvent, String> {
    // This is used to return the key of the events so that we have KeyedStream from the datasource.
    @Override
    public String getKey(BTSAlarmEvent value) throws Exception {
        return value.station_id;
    }
}
