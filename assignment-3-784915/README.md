# Assignment 3 - 784915

* Here is the full structure of my assignment:
```
.
├── README.md
├── assignment3.pdf
├── code
│   ├── Makefile
│   ├── client
│   │   ├── consume.py
│   │   ├── customerstreamapp
│   │   │   ├── dependency-reduced-pom.xml
│   │   │   ├── pom.xml
│   │   │   ├── src
│   │   │   │   └── main
│   │   │   │       ├── java
│   │   │   │       │   └── analytics
│   │   │   │       │       ├── AlarmKeySelector.java
│   │   │   │       │       ├── BTSAlert.java
│   │   │   │       │       ├── BTSError.java
│   │   │   │       │       ├── BTSEvent.java
│   │   │   │       │       ├── BTSParser.java
│   │   │   │       │       ├── CustomerStreamApp.java
│   │   │   │       │       ├── GlobalStatisticsFunction.java
│   │   │   │       │       ├── MyProcessWindowFunction.java
│   │   │   │       │       ├── Statistics.java
│   │   │   │       │       └── StatisticsKeySelector.java
│   │   │   │       └── resources
│   │   │   │           └── log4j.properties
│   │   │   └── target
│   │   │       ├── CustomerStreamApp-0.1-SNAPSHOT.jar
│   │   │       ├── classes
│   │   │       │   ├── analytics
│   │   │       │   │   ├── AlarmKeySelector.class
│   │   │       │   │   ├── BTSAlert.class
│   │   │       │   │   ├── BTSError.class
│   │   │       │   │   ├── BTSEvent.class
│   │   │       │   │   ├── BTSParser.class
│   │   │       │   │   ├── CustomerStreamApp$1.class
│   │   │       │   │   ├── CustomerStreamApp.class
│   │   │       │   │   ├── GlobalStatisticsFunction.class
│   │   │       │   │   ├── MyProcessWindowFunction.class
│   │   │       │   │   ├── Statistics.class
│   │   │       │   │   └── StatisticsKeySelector.class
│   │   │       │   └── log4j.properties
│   │   │       ├── generated-sources
│   │   │       │   └── annotations
│   │   │       ├── maven-archiver
│   │   │       │   └── pom.properties
│   │   │       ├── maven-status
│   │   │       │   └── maven-compiler-plugin
│   │   │       │       └── compile
│   │   │       │           └── default-compile
│   │   │       │               ├── createdFiles.lst
│   │   │       │               └── inputFiles.lst
│   │   │       └── original-CustomerStreamApp-0.1-SNAPSHOT.jar
│   │   ├── perf_test.py
│   │   ├── perf_toggle_Ntimes.py
│   │   ├── produce.py
│   │   ├── result_analytics.log
│   │   └── toggle.py
│   ├── docker-compose.yml
│   ├── mysimbdp-coredms
│   │   ├── init_db.py
│   │   └── split_dataset.py
│   └── requirements.txt
├── data
│   ├── README.md
│   ├── bts-data-alarm-2017.csv
│   ├── sorted_bts-data-alarm-2017.csv
│   └── subdatasets
│       ├── subdataset_1.csv
│       ├── subdataset_10.csv
│       ├── subdataset_11.csv
│       ├── subdataset_12.csv
│       ├── subdataset_13.csv
│       ├── subdataset_14.csv
│       ├── subdataset_15.csv
│       ├── subdataset_16.csv
│       ├── subdataset_17.csv
│       ├── subdataset_18.csv
│       ├── subdataset_19.csv
│       ├── subdataset_2.csv
│       ├── subdataset_20.csv
│       ├── subdataset_21.csv
│       ├── subdataset_22.csv
│       ├── subdataset_23.csv
│       ├── subdataset_24.csv
│       ├── subdataset_25.csv
│       ├── subdataset_26.csv
│       ├── subdataset_27.csv
│       ├── subdataset_28.csv
│       ├── subdataset_29.csv
│       ├── subdataset_3.csv
│       ├── subdataset_30.csv
│       ├── subdataset_31.csv
│       ├── subdataset_32.csv
│       ├── subdataset_33.csv
│       ├── subdataset_34.csv
│       ├── subdataset_35.csv
│       ├── subdataset_36.csv
│       ├── subdataset_37.csv
│       ├── subdataset_38.csv
│       ├── subdataset_39.csv
│       ├── subdataset_4.csv
│       ├── subdataset_40.csv
│       ├── subdataset_41.csv
│       ├── subdataset_42.csv
│       ├── subdataset_43.csv
│       ├── subdataset_44.csv
│       ├── subdataset_45.csv
│       ├── subdataset_46.csv
│       ├── subdataset_47.csv
│       ├── subdataset_5.csv
│       ├── subdataset_6.csv
│       ├── subdataset_7.csv
│       ├── subdataset_8.csv
│       └── subdataset_9.csv
├── logs
│   └── github.log
├── reports
│   ├── Assignment-3-Deployment.md
│   ├── Assignment-3-Report.md
│   └── figures
│       ├── schema.drawio
│       └── schema.png
├── selfgrading.csv
└── submitter.csv
```
