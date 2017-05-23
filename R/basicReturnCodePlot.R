#*****************************************************************
##  Filename    :   basicSuccessPlot.R 
##  Author      :   Ileana streinu
##  Date		: 	19 Feb 2017
##  Updated		:   
#*****************************************************************
#
# Basic filename vs. runtime plot script
# for data extracted form a basic surveyResults.csv file
#

print("===================== Start basicSuccessPlot.R ")

args <- commandArgs(trailingOnly = TRUE)

csvFilePath <- args[1]			# path to surveyResults.csv file
outputFolderPath <- args[2]		# path to "plots" folder in step folder

# csv_file_contents <- read.csv(csvFilePath)
execution_data <- read.table(csvFilePath,header=T, sep=",")

print("========== Contents of the input surveyResults.csv file = ")
print(execution_data)
print("=========================")

outputFile <- "plotPie.png"

setwd(outputFolderPath);

# Start PNG device driver to save output to plot.png		
png(filename=outputFile)
# png(filename=outputFile,height=295, width=300, bg="white")

max_y <- max(execution_data$Return.Code)
if (max_y < 1) max_y <- 1
min_y <- min(execution_data$Return.Code)
if (min_y > -1) min_y <- -1
xlabs <- execution_data$Filename

yticks <- execution_data$Return.Code

# round2 <- function(x){
# 	rx <- round(x,digits=2)
# 	return(rx)
# 	}

eliminate_duplicates <- function(list){
	dup<-duplicated(list) 	# indicates position of duplicates
	sList<- list[!dup] 	# simple list sList: retain only positions matching FALSE in dup
	return(sList)
}

yticks_unique <- eliminate_duplicates(yticks)

plot(execution_data$Return.Code, type="o", col="blue", 
   ylim=c(min_y,max_y), axes=FALSE, ann=FALSE)
   
axis(1, las=2, at=1:length(xlabs), lab=xlabs)
# axis(2, las=1, at=yticks_unique)
axis(2, las=1, at=min_y:max_y)
box()

title(xlab= "Filename", col.lab=rgb(0,0.5,0))
title(ylab= "Return Code", col.lab=rgb(0,0.5,0))

title(main="Filename vs. Return Code", col.main="red", font.main=4)


dev.off()

print("=======================  End basicSuccessPlot.R ")
