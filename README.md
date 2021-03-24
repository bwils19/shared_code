# Automated Raw Data Testing
### Video Demo: https://youtu.be/ZGUDi1wS_mk
### Description:

So I totally get that the title of this project sounds boring as hell and to most it probably is. But for me this project has become quite useful and actually saved me time and money. I'm also really excited about it.

#### Background
I get daily raw data from an independent data source automatically placed into an aws s3 location. It would be great if I could completely trust this data source that
they are going to give me good and enough data everyday, but I can't trust them, or won't rather. Everyday I had been manually checking 4 things with this data; total volume of data, fill rate of a particularly important field,
number of files they put in the s3 location, and the average file size of the files they put in (they put many in each day). There had to be an easier way than doing this manually.

#### Summary of code:
So instead of spending an hour or so each morning running through these mundane steps just to ensure that I recieved good data, I decided to automate. I chose to write the automation script in python since that is what I've
enjoyed using the most up to now. The script contains 1 class with 5 functions (6 counting the "__init__" function). In the init function I assign all necessary varibles needed throughout the scirpt such as aws parameters, the date
that I want to pull from (I chose to pull the previous 2 weeks as a comparison for the day. This can easily be adjusted.), and the Athena SQL queries I want to use. I have 2 Athena queries, one that returns the total volume count of
the data as well as the distinct id count (this id value can have many duplicates) and another that will return the distinct count and the total count of the specific field I want to check.

The first function, **data_checks**, calls a couple of the other functions. The first thing that it does is call the function that runs the queries and gets the results back. It takes those results and calculates the % missing and adds a
column in the data frame for those values. Next it uses a boto3 s3 resource to connect to s3 and count the number of files in each location for the previous 14 days. Then it calculates the average file size in MB for each file in the bucket
for each day. This function then populates a dataframe with the date, number of files, and average file size for the past 2 weeks. At this point, we now have 3 dataframes. One with the total counts and total distinct counts of records, another
with the count of missing values of our chosen important field with the percent missing column populated, and lastly a dataframe with the file count and size for everyday from the past 2 weeks.

The functions the **data_checks** calls are **daterange** and **query_runner**. **daterange** just calculates the data range in which I want to check the S3 files. **query_runner** takes a query as an argument and will run that query in
athena and return the results as a pandas dataframe. I noticed that sometimes athena would timeout on my queries so I added a try/except statement. But one day that I was testing it got completely stuck and just kept trying to run the query
for a few hours. So I added a *trys* counter where it would timeout after 5 tries. This function uses the pyathena connect package as well as pandas to return as a dataframe with column names.

Next I wanted to visualize all of this, so I created a plot function. It took me a while to get this to look clean, but I think it finally did. It puts all four plots in one figure so it's easy to see. I put the total counts and distinct
counts on the same plot (which also took me a while to figure out) with separate axis. Within this function I also compile an .xlsx file of the dataframes.

Lastly, I wasn't quite sure where to put all of this information at first. So I started exploring the python package *email*. This allowed me to compile an email within python in my last function **send_daily_report**. The only argument that it
takes is the compiled figure. It emails me the figure as well as the excel file. I scheduled all of this on a crontab on my computer and now in the mornings I have an email review of the data I received over night!