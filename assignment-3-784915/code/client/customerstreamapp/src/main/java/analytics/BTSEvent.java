/*
 * CS-E4640
 * Linh Truong
 * Edited by Antoine Louis
 */
package analytics;

import java.util.Date;


public class BTSEvent {

    // Class variables
    public String station_id;
    public String datapoint_id;
    public String alarm_id;
    public Date event_time;
    public float value;
    public float valueThreshold;
    public boolean isActive;
    public boolean isDeserialized;
    public String errorLine;

    // Class constructors
    BTSEvent() {}
    
    BTSEvent(String station_id, String datapoint_id, String alarm_id, Date event_time, Float value, Float valueThreshold, Boolean isActive) {
        this.station_id = station_id;
        this.datapoint_id = datapoint_id;
        this.alarm_id = alarm_id;
        this.event_time = event_time;
        this.value = value;
        this.valueThreshold = valueThreshold;
        this.isActive = isActive;
        this.isDeserialized = true;
        this.errorLine = null;
    }

    BTSEvent(String errorLine) throws Exception {
        this.isDeserialized = false;
        this.errorLine = errorLine;
    }
}
