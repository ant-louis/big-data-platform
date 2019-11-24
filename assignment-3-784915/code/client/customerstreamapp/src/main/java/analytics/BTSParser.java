package analytics;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVRecord;
import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.util.Collector;

import java.io.StringReader;
import java.text.SimpleDateFormat;
import java.util.Date;


public class BTSParser implements FlatMapFunction<String, BTSEvent> {
    @Override
    public void flatMap(String line, Collector<BTSEvent> out) throws Exception {

            CSVRecord record = CSVFormat.RFC4180.withIgnoreHeaderCase().parse(new StringReader(line)).getRecords().get(0);

            try {
                // Get elements of record
                String station_id = record.get(0);
                String datapoint_id = record.get(1);
                String alarm_id = record.get(2);
                SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss z");
                Date event_time = format.parse(record.get(3));
                Float value = Float.valueOf(record.get(4));
                Float valueThreshold = Float.valueOf(record.get(5));
                Boolean isActive = Boolean.valueOf(record.get(6));

                // Create the event
                BTSEvent event = new BTSEvent(station_id, datapoint_id, alarm_id, event_time, value, valueThreshold, isActive);
                out.collect(event);
            }
            catch (Exception e) {
                // Create special event for deserialisation error
                BTSEvent event = new BTSEvent("Deserialization error for the line: '"+line+"'");
                out.collect(event);
            }  
    }
}
