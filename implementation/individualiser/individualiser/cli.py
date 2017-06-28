import os.path
import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plot
from clint.textui import puts, colored, indent
import utility_functions as util
import pca_functions as pc


puts(colored.green("\nIndividualiser Test CLI \n======================="))

print "\nPreparing input matrix from CIPIC data..."
#prepare database data input matrix

print "\nRunning PCA and preparing PCWs for manipulation..." 
#call PCA function
#print each component and the variance they represent


while 1 != 2:
    #FIRST, GENERATE MEASURED HRTF GRAPH AS REFERENCE
    print "\nWould you like to generate a reference graph from a measured HRTF/HRIR? (yes/no)"
    gen_reference = raw_input()
    if gen_reference == "yes":
        print "\nFirst select a subject from the CIPIC database for reference:" 
        subject_reference = raw_input()
        while len(subject_reference) < 3:
            puts(colored.red("Subjects in the CIPIC database are labeled with 3 digit numbers (padded from left with zeros)"))
            subject_reference = raw_input()
        subject_data = sio.loadmat("../hrtf_data/CIPIC/CIPIC_hrtf_database/standard_hrir_database/subject_"+subject_reference+"/hrir_final.mat")
     
        #now select azimuth/elevation/side of head
        print "\nLeft or right side? (l/r):"
        sideRef = raw_input()
        subject_data = subject_data['hrir_'+sideRef]
        print "\nNext select an azimuth direction (0-24)"
        azimuth_reference = raw_input()
        print "\nNow an elevation level (0-49):"
        elev_reference = raw_input()
        selected_hrir = subject_data[azimuth_reference][elev_reference]
        print "\nDisplay as HRTF as well as HRIR? (yes/no)"
        hr = raw_input()
        with indent(2, quote='>'):
            puts("subject: "+colored.red(subject_reference))
            puts("azimuth: "+colored.red(azimuth_reference))
            puts("elevation: "+colored.red(elev_reference))
            if hr == "yes":
                puts("as hrtf?: "+colored.red("yes"))
            else:
                puts("as hrtf?: "+colored.red("no"))

        if hr == "yes":
            tmp_hrtf = np.fft.rfft(selected_hrir)
            selected_freq = np.fft.rfftfreq(len(selected_hrir), d=1./44100)#frequency spectrum, should be useful for acis labels?
            selected_hrtf = np.fft.rfft(selected_hrir)
            print "selected_hrtf size:"
            print selected_hrtf.size
            print selected_freq

            f1 = plot.figure()
            ax1 = f1.add_subplot(111)
            ax1.plot(selected_freq, abs(selected_hrtf))
            ax1.set_title("HRTF")
            #ax1.xlabel('frequency')
            #ax1.ylabel('magnitude?')

        f2 = plot.figure()
        ax2 = f2.add_subplot(111)
        ax2.plot(selected_hrir)
        ax2.set_title("HRIR")
        #ax2.ylabel('magnitude?')
        #ax2.xlabel('time (ms)')

        #show either one or both plots
        plot.show(block=False)
    elif gen_reference == 'no':
        sideRef = 'l'
        azimuth_reference = 0
        elev_reference = 0
    
    #NOW PCA A SINGLE HRTF
    print "\nPreparing single-hrtf input matrix for PCA"
    database = util.fetch_database('cipic')
    avg_hrir = util.average_hrtf(database)
    fftd = util.fourier_transform(avg_hrir, False, False)
    avg_hrtf = fftd[0]
    pca_data = util.restructure_data(avg_hrtf, False)
    
    print "\nPlotting results:"
    f3 = plot.figure()
    ax3 = f3.add_subplot(111)
    ear = 0
    if sideRef == 'l':
        ear = 0
    elif sideRef == 'r':
        ear = 1
    ax3.plot(selected_freq, abs(avg_hrtf[ear][azimuth_reference][elev_reference]))
    ax3.set_title("average HRTF")
    plot.show(block=False)

    print "\nPreparing principal components and weights"
    pca_model = pc.train_model(pca_data, 10)
    print "\nPCA model trained"
    pca_data_transformed = pc.pca_transform(pca_model, pca_data)
    print "\nInput matrix transformed, new shape:"
    print pca_data_transformed.shape
    
    while 1 != 2: 
        print "\nEnter the index of the source position you'd like to modify:"
        position = raw_input()
        print "\nCurrent component values:"
        print pca_data_transformed[position]
        
        while 1 != 2:
            print "\nEnter the component you'd like to modify"
            component = raw_input()
            
            print "\nComponent value is currently:"
            print pca_data_transformed[position][component]
            print type(pca_data_transformed[position][component])

            print "\nEnter the new value:"
            value = np.float64(raw_input())

            pca_data_transformed.put([position, component], value)
            print "\nNew component value is:"
            print pca_data_transformed[position][component]
            
            print "\nUpdate another component?"
            n = raw_input()
            if n == "no":
                break

        print "\nReconstructing individualised HRTF from PCWs..."
        pca_data = pc.pca_reconstruct(pca_model, pca_data_transformed)
        custom_hrtf = util.restructure_inverse(pca_data, False)
        #display graph from directionRef of new HRTF
        f4 = plot.figure()
        ax4 = f4.add_subplot(111)
        ax4.plot(selected_freq, abs(custom_hrtf[ear][azimuth_reference][elev_reference]))
        ax4.set_title("customised HRTF")
        plot.show(block=False)
        print "\n Modified hrtf graph for same direction as above"
        
        print "\nWould you like to make any further adjustments? (yes/no)"
        m = raw_input()
        if m == "no":
            break
