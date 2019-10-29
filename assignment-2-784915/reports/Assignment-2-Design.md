# Design report

## Part 1 - Ingestion with batch
### 1. Defining ingestion constraints
Each user of the data platform **mycorebdp** will have a simple configuration file with the following parameters:
| Parameter           | Description     |
|--------------|---------------|
| client_id | Unique id for the client |
| client_pwd | Passwrod of the client|
| max_files | The maximum number of files that the client can ingest into the platform. This could vary depending on some membership.|
| count_files | The current number of files that the client is storing |
| max_size | The maximum total size that the client can store in the database (in MB). This could vary depending on some membership.|
| count_size | The current size that the client is using (in MB)|
| extension | The type of file that the client can push to the platform |

An example of a configuration file can be found below.
~~~json
{
    client_id:"john_doe",
    client_pwd:"1234",
    max_files:10,
    count_files:1,
    max_size:10,
    count_size:7,
    extension:"csv"
}
~~~


### 2. 


### 3. 


### 4. 


### 5. 



## Part 2 - Near-realtime ingestion

### 1. 

### 2. 


### 3. 


### 4. 


### 5. 


## Part 3 - Integration and Extension

### 1. 



### 2. 


### 3. 


### 4. 



### 5. 