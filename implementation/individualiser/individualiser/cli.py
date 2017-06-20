import numpy as np
import matplotlib as plot


print "\nIndividualiser Test CLI \n=======================\nFirst of all, please select a subject from the CIPIC database:" 

subjectRef = raw_input()

print "\nPlease select a direction to view as reference:"

directionRef = raw_input()

#plot this direction and display as an HRTF and/or HRIR

print "\nRunning PCA and preparing PCWs for manipulation..." 

#prepare database data input matrix
#call PCA function
#print each weight, and the variance they represent
#print resulting weight matrix

print "\nReconstructing new HRTF from PCWs..."
#call reconstruction function
#display graph of new HRTF based on directionRef

while 1 != 2:

    while 1 != 2: 
        print "\nEnter the index of the weight you would like to adjust:"
        raw_input()
    
        print "\nEnter the new weight value:"
        raw_input()
        #print confirmation here
    
        print "\nWould you like to adjust any other weights? (yes/no)"
        n = raw_input()
        if n == "no":
            break

    print "\nReconstructing individualised HRTF from PCWs..."
    #call reconstruction function
    #display graph from directionRef of new HRTF

    print "\nWould you like to make any further adjustments?"
    m = raw_input()
    if m == "no":
        break
