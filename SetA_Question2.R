#Author: Timothy Lentz
#version: R version 4.2.2 (2022-10-31 ucrt)
#Input: sales.csv, sd_mapping.csv
#Output: quarterlyPerformance.csv

#open both data files and store them in data frames
salesCSV = read.csv("sales.csv")
sdCSV = read.csv("sd_mapping.csv")

#message the user
print("Analyzing sales.csv and sd_mapping.csv...")

#merge both data frames where PARENT_ACCOUNT_ID == PARENT_ID
both = merge(salesCSV,sdCSV, by.x = "PARENT_ACCOUNT_ID", by.y = "PARENT_ID")

#replace the dates with their respective quarter
both["DATE"][both["DATE"] < "04"] = "2021Q1"
both["DATE"][both["DATE"] < "07"] = "2021Q2"
both["DATE"][both["DATE"] < "10"] = "2021Q3"
both["DATE"][both["DATE"] < "13"] = "2021Q4"

#replace the sd names with an index number
both["SD_NAME"][both["SD_NAME"] == "AMERISOURCE"] = 1
both["SD_NAME"][both["SD_NAME"] == "CARDINAL"] = 2
both["SD_NAME"][both["SD_NAME"] == "MCKESSON"] = 3
both["SD_NAME"][both["SD_NAME"] == "-"] = 4

#create a data frame to output the results
outputData = data.frame(
  "Specialty Distribution" = c("AMERISOURCE", "CARDINAL", "MCKESSON", "NO_CONTRACT_SD"),
  "2021Q1" = c(0,0,0,0),
  "2021Q2" = c(0,0,0,0),
  "2021Q3" = c(0,0,0,0),
  "2021Q4" = c(0,0,0,0),
  check.names = FALSE
)

#fill the output data frame with the relevant information
for (x in 1:nrow(both)){
  outputData[both[x, "SD_NAME"], both[x, "DATE"]] = both[x, "TOTAL_TRX"] + outputData[both[x, "SD_NAME"], both[x, "DATE"]]
}

#print the output data
print(outputData)

#message the user
print("Producing quarterlyPerformance.csv...")

#create a csv file
write.csv(outputData, "quarterlyPerformance.csv", row.names=FALSE)

#message the user
print("Done.")

Sys.sleep(10)

