package analytics;


public class Statistics {

    // Class variables
    public long counter; //Count the number of events for a special key
    public long active_counter; //Count the number of events for a special key where alarm is active
    public double min; //Keep track of the min value for a special key
    public double max; //Keep track of the max value for a special key
    public double mean; //Keep track of the mean value for a special key

    // Class constructors
    Statistics() {
        this.counter = 0;
        this.active_counter = 0;
        this.min = Double.POSITIVE_INFINITY;
        this.max = Double.NEGATIVE_INFINITY;
        this.mean = 0;
    }


    Statistics(Long counter, Long active_counter, Float min, Float max, Float mean) {
        this.counter = counter;
        this.active_counter = active_counter;
        this.min = min;
        this.max = max;
        this.mean = mean;
    }

}
