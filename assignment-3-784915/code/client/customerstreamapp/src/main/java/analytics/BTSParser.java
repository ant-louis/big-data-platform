package analytics;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVRecord;
import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.util.Collector;

import java.io.StringReader;
import java.text.SimpleDateFormat;
import java.util.Date;


public class BTSParser implements FlatMapFunction<String, BTSAlarmEvent> {
    // Simple way to parsing the text as csv record
    @Override
    public void flatMap(String line, Collector<BTSAlarmEvent> out) throws Exception {
        CSVRecord record = CSVFormat.RFC4180.withIgnoreHeaderCase().parse(new StringReader(line)).getRecords().get(0);

        // Just for debug
        //System.out.println("Input: " + line);

        // Filter all records with isActive =false
        if (Boolean.valueOf(record.get(6))) {
            SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss z");
            Date date = format.parse(record.get(3));
            BTSAlarmEvent alarm = new BTSAlarmEvent(record.get(0), record.get(1), record.get(2), date, Float.valueOf(record.get(4)), Float.valueOf(record.get(5)));
            out.collect(alarm);
        }
    }
}