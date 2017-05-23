#*****************************************************************
##  Filename    :   pieChartCreator.R 
##  Author      :   Rebecca Rohrlich & Ileana streinu
##  Date		: 	3 March 2017
##  Updated		:   16 March 2017 by Ileana
#*****************************************************************
#
# Basic filename vs. runtime plot script
# for data extracted from a basic surveyResults.csv file
#
# Creates pie charts based on survey results
# from CSV file. (Equivalence classes based on
# return code for each test-file.)
#
# INPUT: a csv file containing survey results.
# OUTPUT: a pie chart visualization of the data.
#********************************************

args <- commandArgs(trailingOnly = TRUE)

csvFilePath <- args[1]			# path to surveyResults.csv file
outputFolderPath <- args[2]		# path to "plots" folder in step folder

print("===================== START pieChartCreator.R ")

execution_data <- read.table(csvFilePath,header=T, sep=",")
outputFile <- "pieChart.png"
setwd(outputFolderPath);

# Start PNG device driver to save output to plot.png
png(filename=outputFile)
# png(filename=outputFile,height=295, width=300, bg="white")

returnCodes <- execution_data$Return.Code
totalNumTrials <- length(returnCodes)

types <- c()

# create pie chart
library(MASS)
listsForEachError <- split(returnCodes, factor(returnCodes), drop=TRUE)
# print(factor(returnCodes))
typesOfErrors <- lapply(listsForEachError, function(x) {x[1]})
errorSubTotals <- sapply(listsForEachError, function(x) {length(x)}, simplify=TRUE)
# print(errorSubTotals)
percentages <- lapply(errorSubTotals, function(x) {x/totalNumTrials})
# print(percentages)
sliceNames <- paste("Error Code: ",typesOfErrors,"\n Percentage: ", percentages)
pie(errorSubTotals, labels = sliceNames, col = rainbow(length(sliceNames)), main="Run: Success Results")

print("===================== END pieChartCreator.R ")

dev.off()

