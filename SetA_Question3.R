#Author: Timothy Lentz
#version: R version 4.2.2 (2022-10-31 ucrt)
#Input: sample_dx.csv
#Output: cohort.csv

#open the data file
data = read.csv("sample_dx.csv")

#message the user
print("Analyzingsample_dx.csv...")
print("Producing cohort.csv...")

#Define the groups of diagnoses for the cohort
groupA = list("C83.0", "C83.00", "C83.01", "C83.02", "C83.03")
groupB = list("C91", "C91.1", "C91.10", "C91.11", "C91.12")
groupC = list("C95.10", "C95.90")

#Remove unnecessary data from the table
data["prescriber_id"] = NULL

#create subset of data with diagnoses from the cohort
data = subset(data, claim_code %in% c(groupA, groupB, groupC))

#remove duplicate patients from the cohort
cohort = data["patient_id"][!duplicated(data["patient_id"]), ]

#output a csv file with the names of patients in the cohort
patient_id = data.frame(cohort)
colnames(patient_id) = "Patient Id"
write.csv(patient_id, "cohort.csv", row.names=FALSE)

#replace diagnoses codes with their respective group
for(x in 1:length(groupA)){
  data["claim_code"][data["claim_code"] == groupA[x]] = "A"
}
for(x in 1:length(groupB)){
  data["claim_code"][data["claim_code"] == groupB[x]] = "B"
}
for(x in 1:length(groupC)){
  data["claim_code"][data["claim_code"] == groupC[x]] = "C"
}

#replace dates with their respective month
for (x in 1:nrow(data)){
  data[x, "service_date"] = substr(data[x, "service_date"],1,1)
}

#create a subset of the data for each group
dataA = subset(data, claim_code == "A")
dataB = subset(data, claim_code  == "B")
dataC = subset(data, claim_code == "C")

#merge each subset where patient_id and service_date is equal in both sets
AB = merge(dataA,dataB, by = c("patient_id","service_date"))
AC = merge(dataA,dataC, by = c("patient_id","service_date"))
BC = merge(dataB,dataC, by = c("patient_id","service_date"))

#combine the resulting sets, then remove duplicate patient_ids
total = rbind(AB["patient_id"],AC["patient_id"], BC["patient_id"])
total = total["patient_id"][!duplicated(total["patient_id"]), ]


print(c("The number of patients with diagnoses in different groups in the same month is: ", length(total)))
write.csv(patient_id, "cohort.csv", row.names=FALSE)

print("Done.")

Sys.sleep(15)
