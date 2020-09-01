# k8-test-data

If you are working on this project via Upwork, see also our [Upwork Rules of Engagement](https://github.com/filetrust/Open-Source/blob/master/upwork/rules-of-engagement.md)

### Project brief

**Objective**: Test data for GW Rebuild engine running in the multiple K8 Projects

- In order to effectively test the K8 projects, we need a sufficient test data file, that is able to simulate different type of threats and covering all file types supported by Glasswall. Key activities to be covered are 
  - GitHub repo with thousands of test files to be created. 
  - Proceed with caution when handling live malware files.
  - The file types should cover all supported file types by Glasswall (Refer https://glasswallsolutions.com/technology/ or https://file-drop.co.uk/ )
  - Sample files can be sourced from Glasswall public files(https://engineering.glasswallsolutions.com/docs/products/cloud-sdk/sample-files/ , https://github.com/filetrust/GW-Test-Files , )
  - Glasswall private files (https://github.com/filetrust/malicious-test-files  , https://github.com/filetrust/sdk-eval-toolset/tree/master/test  and  https://console.aws.amazon.com/s3/buckets/jp-testbucket-1/?region=eu-west-2) 

- The final objective is to be able to to support - 4 Million files with an average file size of 10 Mbs. However at start we will start with Github repo. 
  - Scrapper to be designed to fetch files from Glasswall repositories and other public repositories. 
  - A File Validator to validate the malacious content of the file. 
  - A File Handler to persit the files to Github repository. 
  - Dynamic generation of files , based on programmatically modifications of content, structure and capabilities.
  
Malware Public Repositories ( Proceed with caution when handling live malware) :

**VirusShare**: https://virusshare.com/

  - Requires login (free)
  - ZIP password is “infected"

**Contagio**: http://contagiodump.blogspot.com/

  - Requires password (free)
  - Related blog: http://contagiominidump.blogspot.com/

**AVCaesar**: https://avcaesar.malware.lu/

  - Requires login (free)
  - Free accounts can download 15 malware samples/day

**The Zoo**: https://github.com/ytisf/theZoo

  - Look in malwares/Binaries subdirectory
  - ZIP password is “infected"

**Malshare**: https://malshare.com

  - Immediate access - register to get an API key allowing download of 1000 samples/day

**Das Malwerk**: http://dasmalwerk.eu/

  - Immediate access
  - ZIP password is “infected”

Public malware reference - https://cyberlab.pacific.edu/resources/malware-samples-for-students