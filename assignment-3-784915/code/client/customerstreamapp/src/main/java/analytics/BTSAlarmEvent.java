/*
 * CS-E4640
 * Linh Truong
 * Edited by Antoine Louis
 */
package analytics;

import java.util.Date;


public class BTSAlarmEvent {
    // Class variables
    public String station_id;
    public String datapoint_id;
    public String alarm_id;
    public Date event_time;
    public float value;
    public float valueThreshold;
    public boolean isActive;

    // Class constructors
    BTSAlarmEvent() {}
    BTSAlarmEvent(String station_id, String datapoint_id, String alarm_id, Date event_time, Float value, Float valueThreshold, Boolean isActive) {
        this.station_id = station_id;
        this.datapoint_id = datapoint_id;
        this.alarm_id = alarm_id;
        this.event_time = event_time;
        this.value = value;
        this.valueThreshold = valueThreshold;
        this.isActive = isActive;
    }

    // Methods
    public String toString() {
        return "station_id="+station_id + " for datapoint_id=" + datapoint_id + " at " + event_time.toString() + " alarm_id="+alarm_id+" with value =" +value+" and isActive="+isActive;
    }
}
