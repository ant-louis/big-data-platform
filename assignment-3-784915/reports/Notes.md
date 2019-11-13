To start the RabbitMQ run the following command. 
```
rabbitmq-server
```

We can access RabbitMQ web dashboard by going to http://localhost:15672. The default username and password is guest and guest respectively.

To stop RabbitMQ press Ctrl + C. 


I can launch multiple workers (consumers) and with the settings that I put they will dispatch the messages fairly and process the messages. No messages can be lost due to the manual ack that I configured in the callback function. So you have multiple workers dealing that will handle the same queue. 