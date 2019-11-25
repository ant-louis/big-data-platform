/*
 * CS-E4640
 * Linh Truong
 * Edited by Antoine Louis
 */
package analytics;

public class BTSAlert {

    // Class variables
    public String station_id;
    public String datapoint_id;
    public String alarm_id;
    public String counter;
    public String active_counter;
    public String min;
    public String max;
    public String mean;
    public String error;
    public String nbErrors;


    // Class constructors
    public BTSAlert() {}

    public BTSAlert(String error, String nbErrors) {
        this.error = error;
        this.nbErrors = nbErrors;
    }

    public BTSAlert(String station_id, String datapoint_id, String alarm_id) {
        this.station_id = station_id;
        this.datapoint_id = datapoint_id;
        this.alarm_id = alarm_id;
    }

    public BTSAlert(String station_id, String datapoint_id, String alarm_id, String counter, String active_counter, String min, String max, String mean) {
        this.station_id = station_id;
        this.datapoint_id = datapoint_id;
        this.alarm_id = alarm_id;
        this.counter = counter;
        this.active_counter = active_counter;
        this.min = min;
        this.max = max;
        this.mean = mean;
    }


    // Methods
    public String alarmMessage() {
        return "{\"Message Type\":\"WindowStreamingAnalytics\",\"Content\":{\"Station\":"+station_id+",\"Sensor\":"+datapoint_id+",\"Alarm\":"+alarm_id+",\"Message\":\"Alarm often gets triggered!\"}}";
    }


    public String statMessage() {
        return "{\"Message Type\":\"GlobalStreamingAnalytics\",\"Content\":{\"Station\":"+station_id+",\"Sensor\":"+datapoint_id+",\"Alarm\":"+alarm_id+",\"Events counter\":"+counter+",\"Active alarms counter\":"+active_counter+",\"Minimum value\":"+min+",\"Maximum value\":"+max+",\"Mean value\":"+mean+"}}";
    }


    public String errorMessage() {
        return "{\"Message Type\":\"DeserializationError\",\"Content\":{\"Error line\":"+error+",\"Total number of errors\":"+nbErrors+"}}";
    }

}
