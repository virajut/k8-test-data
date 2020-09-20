# Test Data POC

### Usage


## Docker Image



### Build

* Set .env file in each service [ file_distribution and gw_crawler ]

`docker build -t glasswallcrawler:1.0 gw_crawler`
`docker build -t k8-file-distribution file_distribution`


### Run

`docker-compose up`

