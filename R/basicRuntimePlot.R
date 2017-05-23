#*****************************************************************
##  Filename    :   basicRuntimePlot.R 
##  Author      :   Ileana streinu
##  Date		: 	19 Feb 2017
##  Updated		:   
#*****************************************************************
#
# Basic filename vs. runtime plot script
# for data extracted form a basic surveyResults.csv file
#

print("===================== Start basicRuntimePlot.R ")

args <- commandArgs(trailingOnly = TRUE)

csvFilePath <- args[1]			# path to surveyResults.csv file
outputFolderPath <- args[2]		# path to "plots" folder in step folder

# csv_file_contents <- read.csv(csvFilePath)
execution_data <- read.table(csvFilePath,header=T, sep=",")

# print("========== Contents of the input surveyResults.csv file = ")
# print(execution_data)
# print("=========================")

outputFile <- "plot.png"

setwd(outputFolderPath);

# Start PNG device driver to save output to plot.png		
png(filename=outputFile)
# png(filename=outputFile,height=295, width=300, bg="white")

max_y <- max(execution_data$Execution.Time)
xlabs <- execution_data$Filename

yticks <- execution_data$Execution.Time

round2 <- function(x){
	rx <- round(x,digits=2)
	return(rx)
	}

round_and_eliminate_duplicates <- function(list){
	list2 <- round2(list)	# round-off to 2 decimals
	dup<-duplicated(list2) 	# indicates position of duplicates
	sList<- list2[!dup] 	# simple list sList: retain only positions matching FALSE in dup
	return(sList)
}

yticks_rounded_unique <- round_and_eliminate_duplicates(yticks)

plot(execution_data$Execution.Time, type="o", col="blue", 
   ylim=c(0,max_y), axes=FALSE, ann=FALSE)
   
axis(1, las=2, at=1:length(xlabs), lab=xlabs)
axis(2, las=1, at=yticks_rounded_unique)
box()

title(xlab= "Filename", col.lab=rgb(0,0.5,0))
title(ylab= "Running time", col.lab=rgb(0,0.5,0))

title(main="Filename vs. Running time", col.main="red", font.main=4)


dev.off()

print("=======================  End basicRuntimePlot.R ")
