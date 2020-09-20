#k8-test-data

##Test Data Release notes
        Goal : Goal is to fetch malware files from various sites, store it in cloud and distribution of the same using api

        The code does web crawling of Das malverk site https://das-malwerk.herokuapp.com/ and fetches malicious zip 

        It unzips and check for malicious and zip it and store in minio
        
        The app is fetching all malicious zip links from https://das-malwerk.herokuapp.com
        
        Once we get link, we are downloading zip
        
        We are unzipping and sending it to virustotal api to get report
        
        Later the code zips the file and store it in minio.
        
        The web scraper , minio and distribution api will be running in differnet pods and independent of each other
        
##Pedning tasks

        Fetching XML report from virustotal is not implemented since once we send file to virustotal,it will go to queue and report will be generated after some minites. 
        
        Storing zip according to file type is yet to be done.
        
        Persisting transaction in mysql is yet to be completed.



