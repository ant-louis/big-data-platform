# Report

## Part 1 - Design for streaming analytics

### 1. Dataset selection and analytics for the customer

#### Dataset
For this project, I decided to use the BTS dataset provided by BachPhu, a company developing IoT solution in Vietnam. It is a collection of sensors data from base stations. The data structure is as follow:
* *station_id*: the id of the stations
* *datapoint_id*: the id of the sensor (data point)
* *alarm_id*: the id of the alarm
* *event_time*: the time at which the event occurs
* *value*: the value of the measurement of the datapoint
* *valueThreshold*: the threshold set for the alarm. Note that some threshold values are set to a default value of 999999.
* *isActive*: the alarm is active (true) or not (false)
* *storedtime*: no store

Note that the given dataset was split into different smaller datasets, each leveraging data about a given station (split according to the station_id). 

This dataset was chosen for multiple reasons. First of all, it is simple, clean and easy-to-use, and its size is reasonable (25.2 MB). Then, it is a good fit for streaming analytics. Indeed, in each dataset, each row represents a certain data event recorded at a given time (*event_time* represents the timestamp of the data event). Moreover, these data came from sensors that lend themselves well to analytics with near-realtime ingestion being really suitable to sensors.


#### Analytics
Now, let's give some example of analytics that could be performed with our dataset.

**(i) Streaming analytics which analyzes streaming data from the customer**
- Analyzing the frequency of alarms activations in a given station for each sensor. This could help detect which machine in the station might be defective when a high frequency is noticed.
- Checking if an alarm has been set. This simple but nevertheless practical analytics could for example notify the consumer with a warning.
- Analyzing the frequency of incoming data points for each sensor in a given station. This would be useful for detecting missing values due to a time out of the sensor.
- Keeping track of interesting values related to each sensor such as the (online) maximum/minimum/mean value of each sensor in a given station.
- Analyzing the consistency of the data points. This feature would obviously be useful to detect outliers in the incoming data and removing noise. Notice that it either requires a sufficiently large window or comparison could be made with the currently tracked mean value for example.
- ...

**(ii) Batch analytics which analyzes historical results outputted by the streaming analytics**
- Analyzing among all stations which types of alarm have been the most activated during a given period of time.
- Analyzing which stations have the bigger number of alarm activations for a given sensor.
- Analyzing in a given station which sensors activate the most the alarms.
- Analyzing for a given alarm in a given station at which moments of the day it is the most activated.
- ...

In brief, streaming analytics can be very useful for reliability analysis and anomaly detection, while batch analytics can further analyze the outputted statistics by plotting detailed histograms and graphs.


## 2. Discussion about streaming analytics

**(i) Should the analytics handle keyed or non-keyed data streams for the customer data?**

In the case of non-keyed streams, all elements in the stream are processed together and the user-defined function has access to all elements in a stream. At the opposite, in the case of a keyed stream, the stream can be partioned into multiple independent streams by a key. That way, when a window is processed in a keyed stream,the user-defined function only has access to items with the same key. In our case, where each station is equipped with multiple sensors linked to a certain number of alarms, keyed streams seem to be more suitable. Indeed, partitioning the stream according to the *datapoint_id* or *alarm_id* would allow us to gain in accuracy and flexibility in our analytics. We could then adapt the different analytics and window sizes (discussed in Question 3) in each stream in function of the characteristics of the given sensors or alarms, which makes more sense. Another advantage of working with keyed streams is that it allows to parallelize work, which is not possible for non-keyed streams where only one machine in the cluster will be able to execute our code.


**(ii) Which types of delivery guarantees should be suitable?**

Below are listed some guarantees that our platform could give to the customers:
* Handling missing data: three possibilities are discussed below in relation with our type of data.
    - At most once: message loss is possible and no duplication of messages. In failure scenarios, events will be dropped and re-delivery attempts are not made. At first glance, this delivery guarantee does not perfectly match our application for two reasons. First, we are dealing with sensors data that, if a threshold is exceeded, activates an alarm. In real life, the activation of the alarm could be critical and not receiving a message could definitely be a problem. Also, some sensors might not give data points at a high frequency, but maybe just once a day. In that case, one can not afford to lose even one data point for such a low emission frequency.

    - At least once: no message loss but duplication is possible. In event of failure scenarios, re-delivery attempts are made. This delivery guarantee might be a bit more suitable for our application. Indeed, as previously explained, losing messages might be problematic. Now, duplication either might or might not be a problem depending again on the frequency of the emitted data points. If the frequency is high, having duplicates will not false by a lot our analytics (mean for e.g.), but might completely false if one sensor only emits a few data points a day.

    - Exactly once: no message loss and no duplication of messages. For obvious reasons, this delivery guarantee is probably the most suitable for our application. It would ensures not to have the previously mentioned problems. 

- Handling out-of-order data: let's take an example to understand the importance of providing features to handle this problem. Imagine that each time an alarm is activated, customer receives a notification. At a certain time, an alarm is activated and a message is sent. A few seconds later, the situation is stabilised and another message is sent. If the first message arrives after the second one, it will notify the consumer that that alarm is now activated while it is now stabilised, which is problematic.

- Guaranteeing availability: providing fault tolerance features to ensure continuous processing of data by achieving near-realtime response with minimal overhead for high-volume data streams.

- Guaranteeing data safety: ensuring the customers to keep their data safe and private.

- Processing and responding instantaneously: achieving the near-realtime response with minimal overhead for high-volume data streams.

### 3. Types of time and types of windows to consider

**(i) Types of time to consider in stream processing**

The chosen dataset already provides timestamps which characterizes the moment when the measure was taken, i.e. the "application time" (also called the "event time"). We will use them in this project for our stream processing. 

Another alternative would be to re-generate timestamps when the messages arrive in the platform, therefore considering the so-called "arrival time". However, this alternative is far less robust than the previously mentioned one since we would take into account the "message received time" and not the "measure creation time". One can easily figuring out scenarios where this could be a problem for our analytics. For example, let's imagine for an instant that the network crashes for multiple minutes, while the sensors continue to measure values and store them temporarily in a buffer pending an answer for the network. When connection is restored, all the buffered messages are sent together and timestamps are created on the server side when they are received. Now, our streaming analytics might detect the activation of an alarm and send the consumer a warning, while this activation happened minutes ago. This example emphasizing the possible delays in the network shows properly the importance for the timestamps to be created on the device side. In addition, this requirement is also necessary for handling out-of-order data.



**(ii) Types of windows to develop for the analytics**

In this project, I chose to implement sliding windows. Now, two kinds of windows might be considered: timing windows and fixed size windows. A timing window will consider a given interval of time in which the incoming elements will be processed (for e.g., process the elements that came in the last minute). At the opposite, fixed size window will take into account a given number of data points and process these points. Both types of windows might be suitable for our application. However, it also depends on the intrinsic characteristics of the sensors, particularly of their frequency of emission. This strengthens even more my choice to consider keyed streams, as independent windows can be set individually for each sensor. Indeed, if a sensor only emits a few data points every hour, then it wouldn't make any sense to consider a timing window of a few seconds. In that case, a larger interval of time must be considered, or a fixed size window should be chosen.

It is difficult to draw out these types of windows as they both might be suitable for our dataset. In this project, I chose to implement sliding timing windows for a time window of 1 minute, refreshed all 5 seconds.

Notice that in practice, the consumer should also have the choice to impose which kind of windows better match his application, as he is the one to exactly know the data he is sending to the platform.


### 4. Important performance metrics for the streaming analytics

First, we can consider metrics related to time:
* Response time: Indicates the required time for the platform to send a response to the source for a given event (in milliseconds).
* Out-of-order events: Indicates the number of events received out of order, that were either dropped or given an adjusted timestamp. 
* Late input events: Indicates the number of events arriving late from the source (according to a configured arrival tolerance window). This metric can include events that have been dropped or have had their timestamp adjusted.
* Early input events: Indicates the number of events whose timestamp is earlier than their arrival time by more than a given threshold (5 minutes for e.g.).
* Watermark delay: Indicates the delay of the streaming data processing job. It is computed as the wall clock time of the processing node minus the largest watermark it has seen so far.

Then, other useful metrics are:
* Throughput: Indicates the amount of data received by the stream analytics job (in bytes). 
* Input events received: Indicates the number of events received by the platform.
* Deserialization errors: Indicates the number of input events that could not be deserialized.
* Runtime errors: Indicates the total number of errors related to query processing.


Notice that these kinds of metrics are often available in well-known Big Data Platforms such as [Microsoft Azure](https://docs.microsoft.com/en-us/azure/stream-analytics/stream-analytics-time-handling).



### 5. Architecture design

The design of my architecture for the streaming analytics service is shown in the Figure below:

![scheme](figures/schema.png)

#### Pipeline
Here are the different steps of the pipeline:

1. Customer produces data, i.e. sends data points through a continuous flow to his dedicated channel *in1* in the RabbitMQ Message Broker.
2. Then, the customer can decide whenever he wants to start/stop the analytics on his data. Toggling the *start_analytics* script will copy the *customerstreamapp* (implemented by the customer) on the Flink server and begin the stream processing on the Flink server.
3. The Flink job running the *customerstreamapp* of the customer will read data from the input channel of the customer and perform near-realtime analytics on them.
4. Each analytics performed by the *customerstreamapp* running on the Flink server will be sent to the output channel of the customer in the RabbitMQ Message Broker.
5. From there, the consumer is able to consumer the messages arriving in his output channel to explore the computed analytics.
6. Optionally, the analytics performed by the *customerstreamapp* can be stored into the Cassandra database.


#### Customer data sources
In real life, the customer data sources will be sensors that will output data points with a timestamp created when measure is taken. In practice for this project, we will use data points already collected and stored in a *.csv* file. Hence, we will simulate the emission of data points from the sensors by reading the *.csv* file row by row at given interval of time. The original dataset *bts-data-alarm-2017.csv* has been sorted by timestamp in chronological order to reproduce a real-life emission of data points. It has then been split into multiple subdatasets to play with lighter files.


#### Mysimbdp message brokers
RabbitMQ was chosen as the message broker for this project but has not been my first choice. I first tried to implement a streaming pipeline with Apache Kafka + Apache Spark mainly because of the popularity of these tools in the industry. However, I encountered some severe difficulties in the management and connection between the Docker containers of this pipeline, and after multiple days of debugging without solutions, I finally decided to give a chance at RabbitMQ with Flink as streaming analytics service. 

It turned out that RabbitMQ might have some advantages over Kafka: 
* It offers a variety of features to trade off performance with reliability, including persistence, delivery acknowledgements publisher confirms, and high availability.
* It is true streaming, contrary to Kafka which actually performs micro-batching.
* Deployment is easier and lighter than with Kafka, which requires Zookeeper to work properly, so involves to run an extra container.
* It has highly available queues that can be mirrored across several machines in a cluster, ensuring that even in the event of hardware failure your messages are safe.
* It supports messaging over a variety of messaging protocols.
* It offers great clustering, where several RabbitMQ servers on a local network can be clustered together, forming a single logical broker. 


In my configuration, each customer has exactly two channels in the RabbitMQ Message Broker: one input channel for him to send his data points, and one output channel to receive the results of the analytics. RabbitMQ Message Broker is running in a Docker container.



#### Mysimbdp streaming computing service
As RabbitMQ has been chosen as message broker, I decided to use Flink as the streaming service, as it often is a common choice. Moreover, documentation is highly available on the net and the tutorial of Mr. Truong was really helpful. 

Flink is an excellent choice for multiple reasons. First, it supports both stream and batch processing. In addition, it has a sophisticated state management, event-time processing semantics, and exactly-once consistency guarantees for state. Moreover, Flink can be deployed on various resource providers (YARN, Apache Mesos, Kubernetes) but also as stand-alone cluster. It has been configured for high availability and does not have a single point of failure. Finally, it is highly scalable, delivering high throughput and low latency.



#### Customer streaming analytics app
In this project, the customer is expected to implement its own *customerstreamapp* written in the Java programming language and compiled with Maven in order to get a *.jar* file that will run on the Flink server.



#### Mysimbdp-coredms
The mysimbdp-coredms component has been designed as a Cassandra database. Apache Cassandra is a free and open-source, distributed, wide column store, NoSQL database management system designed to handle large amounts of data across many commodity servers, providing high availability and scalability with no single point of failure.  In practice, the Cassandra database of this demo is running as a single node in a Docker container.


## Part 2 - Implementation of streaming analytics

### 1. Implemented structures of the input streaming data, output result and data serialization/deserialization for customerstreamapp

The implementation of the *customerstreamapp* can be found in the *code/client/customerstreamapp* repository. More specifically, all the implemented Java classes are available in *code/client/customerstreamapp/src/main/java/analytics*, and the main class is called *CustomerStreamApp.java*. Let's now describe the pipeline for the processing of an input event, and the progressive transformations of the data stream.


#### Input Data Stream
 First, the input data stream starts from the customer side, where the latter will continuously send data points from his sensors to the platform. In practice, each record sent is serialized as a String respecting the following format:
````
"station_id,datapoint_id,alarm_id,event_time,value,valueThreshold,isActive,storedtime"
```` 
It actually corresponds to one line of the *.csv* dataset used in this project, encoded as a String. In real life, I assume that the sensors will output a String in the same format each time they create a data point. This format is thus the standard format expected by the platform to perform the implemented analytics. Note that the management of a bad format has been handled and is explained later in Point 2.4. The code for the production of data can be found in *code/client/producer.py*.


#### Deserialized Data Stream
Once the platform received a line in the described format, it will deserialize it. The deserialization is performed by applying a *flatMap* on the original input data stream that will parse (*BTSParser.java*) each input String to retrieve the values of the different features and create a *BTSEvent* object whose class variables correspond to these features. As a result, the input data stream is now converted into a data stream of *BTSEvent* objects.

#### Split Data Streams
After having been parsed the stream, the resulting data stream is then split to two data streams: one corresponding to the *BTSEvent* that have been properly created thanks to a String input line encoded in the proper expected format, and another data stream that will only collect the *BTSEvent* objects that were not properly deserialized due to a bad format. Further details are given in Point 2.4.

#### Keyed Data Stream
The latter data stream of valid *BTSEvent* objects will then be converted into a *KeyedStream* with the *keyBy* function taking as argument a *StatisticsKeySelector* object (returning the key associated to a particular *BTSEvent*). This will partition the stream into disjoint partitions, where all records with the same key are assigned to the same partition. As discussed in the first part, this choice was made to perform more precise analytics on specific stations/sensors/alarms. As a key, I chose to to use the concatenation of the *station_id*, *datapoint_id* and *alarm_id* in the following String format:
````
"station_id-datapoint_id-alarm_id"
````
Therefore, the analytics explained in the next sections will be specific to a particular alarm, triggered by a specific sensor in a given station.


#### Windowed Data Stream
From the resulting keyed data stream, the *window* function is applied with a sliding timing window of 1 minute, refreshed every 5 seconds, to create a windowed data stream that will later be processed by the function *MyProcessWindowFunction*.


#### Processed Data Stream
Two kinds of analytics are performed in this project, on two different streams, thanks to the *process* function applied on the streams. First, a function called *MyProcessWindowFunction* is performed on the windowed data stream. In addition, a function *GlobalStatisticsFunction* is performed on the keyed data stream. These two functions are explained in Point 2.2. The processing of either data stream convert them into a final data stream of String that will be outputted on the output channel of the customer. Serialization of the output result is explained in the next point.


#### Serialization and output result
The processing functions, *MyProcessWindowFunction* and *GlobalStatisticsFunction*, will return String objects as the result of their analytics. More specifically, they will create an object *BTSAlert* that will store all the computed analytics. These objects also dispose of functions that will return a *.json* file embedded in a String containing all the computed analytics. Therefore, the final data stream will be a stream of String containing the results of the analytics. The customer, on his side, listens to his output channel and sees on his console the incoming result messages. These messages are also saved in the file *logs/result_analytics.log*, to let the customer analyze properly the outputted results of the analytics.

Examples of the output messages are given in the next point for each function.



### 2. Key logic of functions for processing events/records in customerstreamapp

Two functions were implemented in this project: one performed on the windowed data stream, and another on the keyed data stream.

#### MyProcessWindowFunction
This function is inspired from the tutorial of Mr. Truong. It basically counts the number of time that a given alarm is active for a particular sensor in a given station (key of the keyed stream), and create an alert when it exceeds a given threshold (the threshold is set to 5 in this demo). Hence, when the threshold is exceeded, the function outputs a *.json* file embedded in a String, that has the following format:
````
{"Message Type":"Window Streaming Analytics","Content":{"Station":1161115040,"Sensor":141,"Alarm":312,"Message":"Alarm often gets triggered!"}}
````


#### GlobalStatisticsFunction
This function applies on the keyed data stream, and basically computes statistics about incoming data for each key. The statistics include the following:
* Count the number of incoming events for each key;
* Count the number of incoming events where the alarm was active for each key;
* Store the minimum value for each key;
* Store the maximum value for each key;
* Store the mean value for each key;

These simple statistics may be for useful for the customer at the end of the day. Let's suppose that the customer launch the analytics job at the beginning of the day, and looks at the results at the end of the day. He can quickly analyze the number of times that a sensor triggered a particular alarm in a given station. Making the ratio with the total number of events received from that sensor, he can easily computes the percentage of alarm activation for that sensor. Storing the minimum and maximum value can allow the customer to notice a highly unusual behavior of one of his machine during the day. Finally, the mean value can help him analyze once again if a given machine has behaved normally during the whole day, by taking a mean reference value for example.


Let's now go a bit deeper in the technical details. As this function is applied on the keyed stream, there will be exactly 6 variables to store per key, the mean being computed by storing a sum variable and dividing it by the events counter. In order to manage that, I created a *ValueState* object implemented with the *Statistics* class, i.e. that each key will have their state instance keeping track of their statistics variables. The computations are then quite simple: it comes down to update the counters and the mean, and possibly the min and max variables of the state. Then, after each update (each *BTSEvent* analyzed), the function creates a new *BTSAlert* with the current statistics and call the method *statMessage* of the *BTSAlert* that will return a *.json* file embedded in a string, that has the following format:
````
{"Message Type":"Global Streaming Analytics","Content":{"Station":1161115010,"Sensor":121,"Alarm":308,"Events counter":8,"Active alarms counter":4,"Minimum value":240.0,"Maximum value":241.0,"Mean value":240.5}}
````



### 3. Discussion about the test environments, the analytics and its performance observations

#### Tests environment
All the tests were performed in local on my machine, a Macbook Pro (15-inch, 2018) with a processor 2,2 GHz Intel Core i7 6 cores and 16 Go 2400 MHz DDR4 of RAM. The streaming pipeline is implemented with multiple Docker containers, described below:
* *rabbit*: the RabbitMQ Message Broker;
* *cassandra*: the Cassandra database;
* *flink-jobmanager*: the Job Manager for the Flink analytics;
* *flink-taskmanager*: one Task Manager for the Flink analytics;

In order to run the Docker containers, I gave Docker 4 CPUs and 6 Go of RAM.


#### Results of the analytics
The results of the analytics can be found in the file *logs/result_analytics.log*. It shows the result messages of both the *MyProcessWindowFunction* and the *GlobalStatisticsFunction*. These two can be differentiated by the field "Message Type" in the received *.json* files. The message type is set to "WindowStreamingAnalytics" for the result of *MyProcessWindowFunction*, and to "GlobalStreamingAnalytics" for the result of *GlobalStatisticsFunction*. In addition, this *.log* file also contains messages of the type "DeserializationError", which happens when an input line has not been deserialized properly (see next point for further explanations).


#### Performance observations
Flink seems to manage very well the incoming records of the customers, performing near real-time analytics that is observable when user launches to terminal consoles, one that produces (send) the data, and the other that shows the resulting analytics coming from Flink. One can see that these analytics messages are arriving nearly as soon as the data is sent from the customer.


### 4. Presentation of the tests and management of wrong data

#### Tests
As previously mentioned, the testing of the analytics was performed by considering a demo customer who sends data from the BTS dataset to mysimbdp platform and receives the corresponding analytics of his *customerstreamapp*. The result analytics of this demo can be found in the *result_analytics.log* file from the *logs/* repository. These analytics were observed for some chosen data points and proven to be correct.

In addition, the platform was later tested with multiple customers sending at the same time their sensor's data (same dataset consider for ease of the demo) and expecting the analytics from their *customerstreamapp* (same for everyone for ease of the demo) in return. These tests were implemented thanks to two Python scripts: *perf_toggle_Ntimes* that has been executed first and basically launches N Flink jobs in the Docker container, one for each customer (eeach customer having his own input and output queues), and *perf_test.py* that measures the total time that Flink took to send back all the analytics to all customers. Results shown that Flink handled properly the analytics of the customers with nearly no delay. Here is the total time that it took to get the analytics back for all customers (for a demo dataset of 1000 lines):
* With 1 customer (expecting 1000 analytics messages): 1.057348151000042 s
* With 2 customers (expecting 1000 analytics messages each): 1.274434758001007 s
* With 5 customer (expecting 1000 analytics messages): 1.134677820956771 s

Hence, increasing the number of users seems not to modify the responsiveness of Flink that still performs the analytics of each customer in a near real-time delay.


#### Handling wrong data
As previously mentioned, the management of badly formatted input String line is handled within and after the deserialization process. Let's detail the *BTSParser* handle a badly formatted String line.

As a reminder, the *BTSParser* parses a String line to retrieve the values of the different features, and then create a *BTSEvent* with these features. But what happens if an element is missing, or a type doesn't match the expected type of the feature, or the line doesn't even correspond to the expected features but is instead a random text? Well, the creation of the *BTSEvent* in the *BTSParser* is actually encapsulated in a *try-catch*. As a result, if anything goes wrong when the constructor of the *BTSEvent* is called (for one of the reasons mentioned above), the exception is caught. From there, another constructor of *BTSEvent* is called, taking in parameters only one argument: the String line that caused the exception. In addition, a class variable called *isDeserialized* is set to *false*, meaning that a problem occurred during the usual creation of a *BTSEvent* and that a special "error" *BTSEvent* was created. Note that this field is set to *true* when everything went well.

That way, whatever the format of the incoming line, a *BTSEvent* is created and the stream is never interrupted. Now, back to the *CustomerStreamApp* streaming pipeline, the result of the *flatMap* with the *BTSParser* outputs a data stream of *BTSEvent* that will then be split into two *BTSEvent* data streams: one of valid events (checked with the *isDeserialized* instance variable of the event), and the other of invalid events (where a deserialization error occurred due to a bad format, where the *isDeserialized* instance variable of the event is thus set to *false*). The splitting is performed by creating a *SplitStream* by applying the *split* function to the parsed data stream.

As a result, we get a stream of valid *BTSEvent* that can further be processed. The "error" stream is just outputted in the output channel of the customer in a *.json* format to let him know which line was badly formatted. In addition, it also keeps a counter of the number of deserializations errors that happen since the beginning of the analytics job. The outputted message is of the following form:
````
{"Message Type":"DeserializationError","Content":{"Error line":'THIS LINE IS WRONG',"Total number of errors":1}}
````



### 5. Parallelism settings: performance and issues
A Flink program consists of multiple tasks (transformations, data sources, and sinks), where each task is split into a given number of parallel instances for execution, each instance processing a subset of the task’s input data. In this demo, the parallelism was initially set to 1. I tried to increment the level of parallelism but got issues because of the chosen guarantee for message delivery. Indeed, as explained in the Point 1.2, I chose to have "Exactly-Once" delivery messages. This configuration is set up when creating the *StreamExecutionEnvironment* in the *CustomerStreamApp*, but can actually only works when the parallelism is set to 1 when the DataStream is instantiated. Indeed, when using the *RMQSource* class consume messages from RabbitMQ queues, the documentation states that the source must be non-parallel (parallelism set to 1) in order to achieve exactly-once. This limitation is mainly due to RabbitMQ’s approach to dispatching messages from a single queue to multiple consumers. This error was thus to be expected, and in order to solve it, it is necessary to provide a "at-least-once" guarantee in the configuration instead of a "exactly-once".




## Part 3 - Connection
### 1. Design and implementation for storing the analytics into mysimbdp-coredms
The previously presented schema already considered the integration of mysimbdp-coredms into the pipeline. As a reminder, here it is:

![scheme](figures/schema.png)

The sixth step actually consists of storing the computed analytics in a dedicated keyspace in the Cassandra database. 

On the technical side, the (Apache Cassandra Connector)[https://ci.apache.org/projects/flink/flink-docs-stable/dev/connectors/cassandra.html] would be necessary to stream these analytics into the database. In order to integrate the streaming to Cassandra, I would modify a bit my original pipeline. First, I would change the output result of my processing functions (*MyProcessWindowFunction* and *GlobalStatisticsFunction*). As a reminder, these functions now output a String by first creating a new *BTSAlert* event and then calling a class method outputting a *.json* file embedded into a String. Instead of doing that, I would output the analytics as a Tuple, as the Cassandra sinks currently support either Tuple or POJO data types. From there, I could stream the Tuple Data Stream into the *CassandraSink* by performing the desired CQL query with *setQuery*. Then, to send back the analytics to the customer, I would simply need to perform an extra *flatMap* operation on this stream of Tuples to convert them into the *.json* files to get back the stream of String that I have now. This stream will then be added to the RabbitMQ sink as previously.


### 2. Implementation of a batch analytics given historical data stored in mysimbdp-coredms
One possible batch analytics that the customer could perform using the stored streaming analytics would be to analyze for each station which sensor has activated the most alarms during a given period of time. This analytics would be possible thanks to the collected results of the "counter of active events" in the *GlobalStatisticsFunction*. One could think at an interactive dashboard where user could select the station he wants, and this would output an histogram of the sensors that triggered the most alarms during the day. 

For the implementation, I would use an extra server running in a Docker container (simple Debian image for example where Python packages are installed, as well as Cassandra driver). With a simple API, the customer could push and toggle his batch analytics script to the server. These analytics would be Python scripts performing the desired computations by querying the Cassandra database. Once performed, the results of the batch analytics would be sent back to the customer (as a *.json* file containing the results for each station_id in a first time, but later one can think to a user interface with histograms). 


### 3. Triggering the execution of a batch analytics
I think that the simplest and most efficient solution is to trigger the alert from the customer side. More specifically, the customer would first modify his *customerstreamapp* running on Flink to integrate a message alert when the critical event happens. This new processing function could be called *CriticalAlertFunction* and that would output a message of the type *Alert* with the explanation of the alert. For example:
````
{"Message Type":"Alert","Content":{"Type":3,"Message":'Very high rate of alarms detected.'}}
````
Then, the *consume* script of the customer would parse each arriving message by checking if an "Alert" message appears. When it does, it would for example check the corresponding type of this alert and from there, toggle the *batch_analytics* script on the BatchAnalytics Server by passing the type of alert in the POST request to let it know which type of analytics it has to perform.

An updated schema of the whole platform integrating this new feature is shown below:

![scheme_part3](figures/schema_part3.png)

The steps 1 to 6 are exactly the same as explained in Point 1.5. Then, let's explain the additional steps:
* 


### 4. Scaling the streaming analytics service



### 5. Exactly once delivery