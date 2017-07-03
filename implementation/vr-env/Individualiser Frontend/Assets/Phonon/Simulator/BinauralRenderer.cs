//
// Copyright (C) Valve Corporation. All rights reserved.
//

using System;
using System.Runtime.InteropServices;

namespace Phonon
{
    public class BinauralRenderer
    {
        public void Create(Environment environment, RenderingSettings renderingSettings, GlobalContext globalContext)
        {
            HRTFParams hrtfParams = new HRTFParams
            {
				//yoooo I can set custom HRTFS with this set to "Custom"
                type = HRTFDatabaseType.Default,
                hrtfData = IntPtr.Zero, //set to zero always apparently
                numHrirSamples = 0, //the number of samples in my custom hrirs
				//gotta implement these callbacks to be able to use custom hrtfs yo! 
                loadCallback = null, //this should point to a function that loads/fft's hrtfs?
                unloadCallback = null, //called when renderer is destroyed
                lookupCallback = null //points to a function that finds the hrtf based on direction coordinates returning L/R hrtfs
            };

            var error = PhononCore.iplCreateBinauralRenderer(globalContext, renderingSettings, hrtfParams, ref binauralRenderer);
            if (error != Error.None)
                throw new Exception("Unable to create binaural renderer [" + error.ToString() + "]");
        }

        public IntPtr GetBinauralRenderer()
        {
            return binauralRenderer;
        }

        public void Destroy()
        {
            if (binauralRenderer != IntPtr.Zero)
                PhononCore.iplDestroyBinauralRenderer(ref binauralRenderer);
        }

        IntPtr binauralRenderer = IntPtr.Zero;
    }
}