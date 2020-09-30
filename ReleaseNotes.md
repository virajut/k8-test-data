#k8-test-data

##Malware Public Repositories  :

**VirusShare**: https://virusshare.com/

  - Requires login (free)
  - ZIP password is “infected"

**The Zoo**: https://github.com/ytisf/theZoo

  - Look in malwares/Binaries subdirectory
  - ZIP password is “infected"

**Malshare**: https://malshare.com

  - Immediate access - register to get an API key allowing download of 1000 samples/day

**Das Malwerk**: http://dasmalwerk.eu/

  - Immediate access
  - ZIP password is “infected”

Public malware reference - https://cyberlab.pacific.edu/resources/malware-samples-for-students

Note :  http://contagiodump.blogspot.com/ in above public reference not implemented since it is paid service and password for malware zip is not availble


##Test Data Release notes
        Goal : Goal is to fetch malware files from various sites, store it in cloud and distribution of the same using api

        The code does web crawling of Das malverk site https://das-malwerk.herokuapp.com/ and fetches malicious zip 

        The app is fetching all malicious zip links from https://das-malwerk.herokuapp.com
        
        We are downloading only .zip files .
        
        The web scraper , minio and distribution api will be running in differnet pods and independent of each other
        
##Pedning tasks

        Fetching XML report from virustotal is not implemented since once we send file to virustotal,it will go to queue and report will be generated after some minites. 
        
        Storing zip according to file type is yet to be done.
        
        Persisting transaction in mysql is yet to be completed.



