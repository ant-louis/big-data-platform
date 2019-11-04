# Assignment 2 - 784915

* Here is the full structure of my assignment:
```
README.md
├── code
│   ├── Makefile
│   ├── clients
│   │   ├── client1
│   │   │   ├── client-input-directory
│   │   │   │   ├── sample0.txt
│   │   │   │   ├── sample1.csv
│   │   │   │   ├── sample10.csv
│   │   │   │   ├── sample11.csv
│   │   │   │   ├── sample2.csv
│   │   │   │   ├── sample3.csv
│   │   │   │   ├── sample4.csv
│   │   │   │   ├── sample5.csv
│   │   │   │   ├── sample6.csv
│   │   │   │   ├── sample7.csv
│   │   │   │   ├── sample8.csv
│   │   │   │   └── sample9.csv
│   │   │   └── fetchdata.py
│   │   ├── client2
│   │   │   ├── client-input-directory
│   │   │   │   ├── sample0.txt
│   │   │   │   ├── sample1.csv
│   │   │   │   ├── sample10.csv
│   │   │   │   ├── sample11.csv
│   │   │   │   ├── sample2.csv
│   │   │   │   ├── sample3.csv
│   │   │   │   ├── sample4.csv
│   │   │   │   ├── sample5.csv
│   │   │   │   ├── sample6.csv
│   │   │   │   ├── sample7.csv
│   │   │   │   ├── sample8.csv
│   │   │   │   └── sample9.csv
│   │   │   └── fetchdata.py
│   │   ├── fetchdata_demo.py
│   │   ├── ingestmessage.py
│   │   └── performances.py
│   ├── docker-compose.yml
│   ├── mysimbdp-coredms
│   │   └── init_db.py
│   ├── mysimbdp-databroker
│   ├── mysimbdp-server
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── server
│   │       ├── batchingestmanager.py
│   │       ├── dir1
│   │       │   ├── clientbatchingestapp.py
│   │       │   ├── customer_profile.json
│   │       │   └── files
│   │       │       ├── sample1.csv
│   │       │       ├── sample10.csv
│   │       │       ├── sample11.csv
│   │       │       ├── sample8.csv
│   │       │       └── sample9.csv
│   │       ├── dir2
│   │       │   ├── clientbatchingestapp.py
│   │       │   ├── customer_profile.json
│   │       │   └── files
│   │       │       ├── sample1.csv
│   │       │       ├── sample10.csv
│   │       │       ├── sample11.csv
│   │       │       ├── sample8.csv
│   │       │       └── sample9.csv
│   │       ├── init.py
│   │       ├── server.log
│   │       ├── streamingestmanager.py
│   │       └── users.json
│   └── requirements.txt
├── data
│   ├── googleplaystore.csv
│   ├── googleplaystore_clean.csv
│   ├── googleplaystore_user_reviews.csv
│   └── license.txt
├── logs
│   └── performance.log
├── reports
│   ├── Assignment-2-Deployment.md
│   ├── Assignment-2-Design.md
│   ├── Assignment-2-Report.md
│   └── figures
│       ├── barplot_speeds.png
│       ├── barplot_times.png
│       ├── scheme.png
│       └── scheme2.png
├── selfgrading.csv
└── submitter.csv
```
