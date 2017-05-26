#*****************************************************************
##  Filename    :   pieChartCreator.R 
##  Author      :   Rebecca Rohrlich & Ileana streinu
##  Date		: 	3 March 2017
##  Updated		:   25 June 2017 by Ileana & Christina
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
outputFilePath <- args[2]		# path to "plots" folder in step folder

print("===================== START pieChartCreator.R ")
#print("input file = ")
#print(csvFilePath)
execution_data <- read.table(csvFilePath,header=T, sep=",")
#print("execution data = ")
#print(execution_data)
#outputFile <- "pieChart.png"
#print("output file path = ")
#print(outputFilePath)
doubleV <- strsplit(outputFilePath, '/')
singleV <- doubleV[[length(doubleV)]]
outputFile <- singleV[length(singleV)]
outputList <- singleV[length(singleV) - (length(singleV):1)]
outputFolderPath <- paste(outputList, collapse = '/')
setwd(outputFolderPath)

# Start PNG device driver to save output to plot.png
#png(filename=outputFile)
png(filename=outputFile,height=295, width=300, bg="white")

returnCodes <- execution_data$exitCode
#print("return codes = ")
#print(returnCodes)
totalNumTrials <- length(returnCodes)
#print("total number trials = ")
#print(totalNumTrials)

types <- c()
#print(types)
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

