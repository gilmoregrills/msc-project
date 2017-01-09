#written in bad pseudocode obvs
#to do in main file:
#   move root declaration to readraw
#   move ext declaration to readraw
#   make hrtfpath output an outputpathname (where the modified hrtf will be written to)

class hrtf
  public stuff:
    inputpathname = #on instantiation, field is populated with str output from hrtfpath()
    outputpathname
    hrtfdata = #a 2:512 array containing contents read from file at pathname
    function writeraw()
      writes hrtf data to a separate directory
  private stuff:
    readraw function
    hrtfpath function
    
constructor hrtf(elev, azim, select):
  do the azim/elev checks
  then do the normal getting-the-right-file-and-making-it-an-array thing
  if (select == 'L'):
        pathname = hrtfpath(root,'full',select,ext,elev,azim)
        larray = readraw(pathname)
        pathname = hrtfpath(root,'full',select,ext,elev,flipazim)
        rarray = readraw(pathname)
        this.hrtfdata = np.vstack((larray, rarray))
  elif (select == 'R'):
        pathname = hrtfpath(root,'full',select,ext,elev,flipazim)
        rarray = readraw(pathname)
        pathname = hrtfpath(root,'full',select,ext,elev,azim)
        larray = readraw(pathname)
        this.hrtfdata = np.vstack((rarray, larray))      
   elif (select == 'H'):
        pathname = hrtfpath(root,'compact',select,ext,elev,azim)
        tmp = readraw(pathname);
        print("this one actually doesn't work")
        
so an hrtf object would have:

hrtf.data = a 2:512 array containing all the hrtf data
hrtf.inputpathname = the file used as input to create this array
hrtf.outputpathname = the file path to be used if calling the writeraw()/writehrtf() function


        
        
  
