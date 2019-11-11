# Report

## Part 1 - Design for streaming analytics

### 1. Dataset selection and analytics for the customer

#### Dataset
This project uses the BTS dataset provided by BachPhu, a company developing IoT solution in Vietnam. It is a collection of sensors data from base stations.
The data structure is as follow:
* *station_id*: the id of the stations
* *datapoint_id: the id of the sensor (data point)
* *alarm_id*: the id of the alarm
* *event_time*: the time at which the event occurs
* *value*: the value of the measurement of the datapoint
* *valueThreshold*: the threshold set for the alarm. Note that some threshold values are set to a default value of 999999.
* *isActive*: the alarm is active (true) or not (false)
* *storedtime*: no store

Note that the given dataset was split into different smaller datasets, each leveraging data about a given station (split according to the station_id). 

This dataset was chosen for multiple reasons. First of all, it is simple, clean and easy-to-use, and its size is reasonable. Then, it is a perfect fit for streaming analytics applications. Indeed, in each dataset, each row represents a certain data event recorded at a given time (*event_time* represents the timestamp of the data event). Moreover, these data came from sensors that lend themselves well to analytics with near-realtime ingestion being really suitable to sensors.


#### Analytics
Now, let's give some example of analytics that could be performed in our application.

**(i) Streaming analytics which analyzes streaming data from the customer**
- Analyzing the frequency of alarms: how often has a given alarm been activated in a given station?
- Analyzing the number of times the threshold of a given sensor has been exceeded: how often has the the threshold of a given sensor been exceeded in a given station?
- Analyzing the frequency of the data points for a given sensor: at which frequency are the data points of a given sensor registered in a given station?
- Analyzing the consistency of the data points: how stable are the values of a given sensor in a given station, are there outliers?
- Analyzing interesting values of a given sensor: what is the current maximum/minimum/mean value of a given sensor for the stream?
- ...

**(ii) Batch analytics which analyzes historical results outputted by the streaming analytics**
- Analyzing among all stations which types of alarm have been the most activated.
- Analyzing which stations have the bigger number of alarm activations for a given sensor.
- Analyzing among all stations which sensor exceeds the most its threshold.
- ...

In brief, streaming analytics is about getting statistics about data analyzed in a given window (frequency, mean, max) for individual stations. On the other hand, batch analytics will analyze these statistics by plotting for example histograms and graphs. 


## 2. Discussion about streaming analytics

**(i) Should the analytics handle keyed or non-keyed data streams for the customer data?**
* In the case of non-keyed streams, all elements in the stream will be processed together and the user-defined function will have access to all elements in a stream. In our case, one can consider that each consumer represents a given station (defined by the station_id) and data has in a sense already been partitioned by this station_id (see Deployment report). Thus, non-keyed streams would be suitable for our application. However, the downside of this stream type is that it gives no parallelism and only one machine in the cluster will be able to execute our code. Hence, we will use keyed streams that are explained just below.

* In the case of a keyed stream, the stream can be partioned into multiple independent streams by a key. For example, our platform could receive data coming from one particular consumer (defined by his *station_id*) but could further be partitioned (for example with the *datapoint_id* or the *alarm_id*). That way, when a window will be processed in a keyed stream, the user-defined function will only have access to items with the same key, hence performing analytics on all elements of a specific key which could allow us to perform more specific computations than when using non-keyed streams. Another advantage of working with keyed streams is that it allows to parallelize work. Finally, the windows could be set specifically for each keyed stream which is really interesting as discussed in Question 3 as, if we decide to group the stream by *sensor_id*, time window would be more suitable for a sensor with a very high emission frequency but a sized window would be a better match for a sensor only emitting a few data points every hour for e.g.


**(ii) Which types of delivery guarantees should be suitable?**

Below are listed some guarantees that our platform could give to the customers:
* Handling missing data: three possibilities are discussed below in relation with our type of data.
    - At most once: message loss is possible and no duplication of messages. In failure scenarios, events will be dropped and re-delivery attempts are not made. At first glance, this delivery guarantee does not perfectly match our application for two reasons. First, we are dealing with sensors data that, if a threshold is exceeded, activates an alarm. In real life, the activation of the alarm could be critical and not receiving a message could definitely be a problem. Also, some sensors might not give data points at a high frequency, but maybe just once a day. In that case, one can not afford to lose even one data point for such a low emission frequency.

    - At least once: no message loss but duplication is possible. In event of failure scenarios, re-delivery attempts are made. This delivery guarantee might be a bit more suitable for our application. Indeed, as previously explained, losing messages might be problematic. Now, duplication either might or might not be a problem depending again on the frequency of the emitted data points. If the frequency is high, having duplicates will not false by a lot our analytics (mean for e.g.), but might completely false if one sensor only emits a few data points a day.

    - Exactly once: no message loss and no duplication of messages. For obvious reasons, this delivery guarantee is probably the most suitable for our application. It would ensures not to have the previously mentioned problems. 

- Handling out-of-order data: let's take an example to understand the importance of providing features to handle this problem. Imagine that each time an alarm is activated, customer receives a notification. At a certain time, an alarm is activated and a message is sent. A few seconds later, the situation is stabilised and another message is sent. If the first message arrives after the second one, it will notify the consumer that that alarm is now activated while it is now stabilised, which is problematic.

- Guaranteeing availability: providing fault tolerance features to ensure continuous processing of data by achieving near-realtime response with minimal overhead for high-volume data streams.

- Guaranteeing data safety: ensuring the customers to keep their data safe and private.

### 3. Types of time and types of windows to consider

**(i) Types of time to consider in stream processing**

The timestamps 



**(ii) Types of windows to develop for the analytics**




timestamp, taille de la window et qu'est ce que je survole (keyed survoler que pour un capteur), l'utilisateur devrait lui-même spécifier quel genre de window il veut (parametres) ou du moins do