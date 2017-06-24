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
    gen_reference = raw_input()
    if gen_reference == "yes":
        print "\nFirst select a subject from the CIPIC database for reference:" 
        subject_reference = raw_input()
        while len(subject_reference) < 3:
            puts(colored.red("Subjects in the CIPIC database are labeled with 3 digit numbers (padded from left with zeros)"))
            subject_reference = raw_input()
        subject_data = sio.loadmat("../databases/CIPIC/CIPIC_hrtf_database/standard_hrir_database/subject_"+subject_reference+"/hrir_final.mat")
     
        #now select azimuth/elevation/side of head
        #print "\nLeft or right side? (l/r):"
        sideRef = "l"#raw_input()
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
            tmp_hrtf = util.fourier_transform(selected_hrir, False);
            selected_freq = tmp_hrtf[1]#frequency spectrum, should be useful for acis labels?
            selected_hrtf = tmp_hrtf[0]
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
    
    #NOW PCA A SINGLE HRTF
    print "\nPreparing single-hrtf input matrix for PCA, shape:"
    database = fetch_database('cipic', True)
    data = util.restructure_data(database, False)
    input_matrix = data[0]
    print input_matrix.shape
    print "\nCreating generalised HRTF, shape:"
    general_hrtf = util.restructure_inverse(input_matrix, False)
    print general_hrtf.shape
    f3 = plot.figure()
    ax3 = f3.add_subplot(111)
    ear = 0
    if sideRef == 'l':
        ear = 0
    else:
        ear = 1
    ax3.plot(selected_freq, abs(general_hrtf[ear][azimuth_reference][elev_reference]))
    ax3.set_title("average HRTF")
    plot.show(block=False)
    print "\nPreparing principal components and weights"
    pca_model = util.train_pca(input_matrix, 10)
    print "\nPCA model trained"
    input_matrix = util.pca_transform(pca_model, input_matrix)
    print "\nInput matrix transformed, new shape:"
    print input_matrix.shape
    
    while 1 != 2: 
        print "\nEnter the index of the source position you'd like to modify:"
        position = raw_input()
        print "\nCurrent component values:"
        print input_matrix[position]
        
        while 1 != 2:
            print "\nEnter the component you'd like to modify"
            component = raw_input()
            
            print "\nComponent value is currently:"
            print input_matrix[position][component]
            print type(input_matrix[position][component])

            print "\nWhat would you like to set it to?"
            value = raw_input()

            input_matrix[position][component] = np.float64(value)
            
            print "\nUpdate another component?"
            n = raw_input()
            if n == "no":
                break

        print "\nReconstructing individualised HRTF from PCWs..."
        output_matrix = util.pca_reconstruct(pca_model, input_matrix)
        output_matrix = util.restructure_inverse(output_matrix, False)
        #display graph from directionRef of new HRTF
        f4 = plot.figure()
        ax4 = f4.add_subplot(111)
        ax4.plot(selected_freq, abs(general_hrtf[ear][azimuth_reference][elev_reference]))
        ax4.set_title("customised HRTF")
        plot.show(block=False)
        print "\n Modified hrtf graph for same direction as above"
        
        print "\nWould you like to make any further adjustments? (yes/no)"
        m = raw_input()
        if m == "no":
            break
