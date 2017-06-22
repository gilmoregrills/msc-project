import os.path
import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plot
from clint.textui import puts, colored, indent
import utility_functions as util


puts(colored.green("\nIndividualiser Test CLI \n======================="))

print "\nPreparing input matrix from CIPIC data..."
#prepare database data input matrix

print "\nRunning PCA and preparing PCWs for manipulation..." 
#call PCA function
#print each component and the variance they represent


while 1 != 2:
    #FIRST, GENERATE MEASURED HRTF GRAPH AS REFERENCE
    print "\nWould you like to generate a reference graph from a measured HRTF/HRIR? (yes/no)"
    genRef = raw_input()
    if genRef == "yes":
        print "\nFirst select a subject from the CIPIC database for reference:" 
        subjectRef = raw_input()
        while len(subjectRef) < 3:
            puts(colored.red("Subjects in the CIPIC database are labeled with 3 digit numbers (padded from left with zeros)"))
            subjectRef = raw_input()
        subjectData = sio.loadmat("../databases/CIPIC/CIPIC_hrtf_database/standard_hrir_database/subject_"+subjectRef+"/hrir_final.mat")
     
        #now select azimuth/elevation/side of head
        print "\nLeft or right side? (l/r):"
        sideRef = raw_input()
        subjectData = subjectData['hrir_'+sideRef]
        print "\nNext select an azimuth direction (0-24)"
        azimuthRef = raw_input()
        print "\nNow an elevation level (0-49):"
        elevRef = raw_input()
        selectedHRIR = subjectData[azimuthRef][elevRef]
        print "\nDisplay as HRTF as well as HRIR? (yes/no)"
        hr = raw_input()
        with indent(2, quote='>'):
            puts("subject: "+colored.red(subjectRef))
            puts("azimuth: "+colored.red(azimuthRef))
            puts("elevation: "+colored.red(elevRef))
            if hr == "yes":
                puts("as hrtf?: "+colored.red("yes"))
            else:
                puts("as hrtf?: "+colored.red("no"))

        if hr == "yes":
            tmpHRTF = util.fourierTransform(selectedHRIR, False);
            selectedFreq = tmpHRTF[1]#frequency spectrum, should be useful for acis labels?
            selectedHRTF = tmpHRTF[0]
            print "selectedHRTF size:"
            print selectedHRTF.size
            print selectedFreq

            f1 = plot.figure()
            ax1 = f1.add_subplot(111)
            ax1.plot(selectedFreq, abs(selectedHRTF))
            ax1.set_title("HRTF")
            #ax1.xlabel('frequency')
            #ax1.ylabel('magnitude?')

        f2 = plot.figure()
        ax2 = f2.add_subplot(111)
        ax2.plot(selectedHRIR)
        ax2.set_title("HRIR")
        #ax2.ylabel('magnitude?')
        #ax2.xlabel('time (ms)')

        #show either one or both plots
        plot.show(block=False)
    
    #NOW UPDATE WEIGHTS
    puts(colored.green("\nWeight matrix:\n============="))
    print ("print weight matrix here")
    #print resulting weight matrix
    while 1 != 2: 
        print "\nEnter the index of the weight you would like to adjust:"
        weight = raw_input()
    
        print "\nEnter the new weight value:"
        value = raw_input()
        
        print "\nUpdating weight:"
        with indent(2, quote='>'):
            puts(colored.red(weight))
        print "To value:"
        with indent(2, quote='>'):
            puts(colored.red(value))

        print "\nWould you like to adjust any other weights? (yes/no)"
        n = raw_input()
        if n == "no":
            break

    print "\nReconstructing individualised HRTF from PCWs..."
    #call reconstruction function
    #display graph from directionRef of new HRTF
    print "new hrtf graph for same direction as above"

    print "\nWould you like to make any further adjustments? (yes/no)"
    m = raw_input()
    if m == "no":
        break
