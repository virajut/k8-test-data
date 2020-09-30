## Run scraper in local machine

## Scraper Sites 

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
  
**Tek Defence** : http://www.tekdefense.com/downloads/malware-samples/
  - Immediate access

###Update .env 

    create virusshare api key from https://virusshare.com/apiv2_reference , 
    
    create malshare api key from https://malshare.com/doc.php,
    
    update .env (see .env_sample)
    
### Run scrapper in Docker
```
    docker build -t glasswallcrawler:1.0 .
     
    docker run --env-file .env glasswallcrawler:1.0 

```











