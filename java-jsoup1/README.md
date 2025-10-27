
# Project Title

One Paragraph of project description goes here



These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.



What things you need to install the software and how to install them

```
Give examples
```



Explain how to run the automated tests for this system

To run all integration tests (runners)
```
mvn verify
```

To run a specific integracion test (specific runner class):
```
mvn verify -Dit.test=com.example.java-jsoup1.runners.CucumberRunnerIT
```

To run all integration tests but filter scenarios by tag:
```
mvn verify -Dcucumber.filter.tags="@web"
mvn verify -Dcucumber.filter.tags="@web or @rest"
mvn verify -Dcucumber.filter.tags="@web and not @rest"
```
  
More information on how to run automated tests can be found [here](https://github.com/veepee-oss/gingerspec/wiki/Running-your-tests)



Explain what these tests test and why

```
Give an example
```



* 0.0.1
    * Work in progress
    


* **John Smith** - *Initial work* -

  
  
This module depends on the GingerSpec framework (QA testing library), where common logic and steps are implemented. 
  
Check more information about the GingerSpec framework [here](https://github.com/veepee-oss/gingerspec/wiki)  