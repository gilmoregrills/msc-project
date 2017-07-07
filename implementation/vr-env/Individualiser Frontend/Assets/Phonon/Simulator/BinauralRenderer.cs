//
// Copyright (C) Valve Corporation. All rights reserved.
//

using System;
using System.Runtime.InteropServices;
using System.Net.Sockets;

namespace Phonon
{
    public class BinauralRenderer
    {
		System.Net.Sockets.TcpClient clientSocket;
		NetworkStream serverStream;
		byte[] output;
		float[,,] leftEarHrir = new float[25, 50, 200];
		float[,,] leftEarHrtf = new float[25, 50, 101];
		float[,,] rightEarHrir = new float[25, 50, 200];
		float[,,] rightEarHrtf = new float[25, 50, 101];

        public void Create(Environment environment, RenderingSettings renderingSettings, GlobalContext globalContext) {
            HRTFParams hrtfParams = new HRTFParams {
				//yoooo I can set custom HRTFS with this set 
				type = HRTFDatabaseType.Custom, //IPL_HRTFDATABASETYPE_CUSTOM
                hrtfData = IntPtr.Zero, //set to zero always apparently
                numHrirSamples = 200, //the number of samples in my custom hrirs
				//gotta implement these callbacks to be able to use custom hrtfs yo! 
				loadCallback = onLoadHrtf, //this should point to a function that loads/fft's hrtfs?
                unloadCallback = null, //called when renderer is destroyed
                lookupCallback = null //points to a function that finds the hrtf based on direction coordinates returning L/R hrtfs
            };

            var error = PhononCore.iplCreateBinauralRenderer(globalContext, renderingSettings, hrtfParams, ref binauralRenderer);
            if (error != Error.None)
                throw new Exception("Unable to create binaural renderer [" + error.ToString() + "]");
        }

		public IntPtr GetBinauralRenderer() {
            return binauralRenderer;
        }

        public void Destroy() {
            if (binauralRenderer != IntPtr.Zero)
                PhononCore.iplDestroyBinauralRenderer(ref binauralRenderer);
        }

		public void onLoadHrtf (int numSamples, int numSpectrumSamples, Phonon.FFTHelper fft, 	System.IntPtr fftHelperData) {
		//I should find a way to call this (replacing the stuff in memory)
		//every time a modification is made to fetch a new custom hrtf
			//how shall we fetch the left and right hrtfs into memory? 
			//then, how should they be processed into HRIRs?
			//open socket, ping 8080, accept byte array
			//transform byte array into normal data array 
			//split into L and R sides
			//manually store those in memory
			//because C# is garbage collected, you gotta mark either methods
			//or sets of variables as 'unsafe'
			output = new byte[2520000];
			clientSocket = new System.Net.Sockets.TcpClient ();
			clientSocket.Connect ("127.0.0.1", 8080);
			serverStream = clientSocket.GetStream ();
			serverStream.Read (output, 0, output.Length);
			output.GetLength (0);//to show dimensions of the array grabbed
			output.GetLength (1);
			output.GetLength (2);

		}

		public void onUnloadHrtf()
		{
			//takes L and R hrir arrays! basically deletes
			//them from memory!!
		}

		public void onLookupHrtf()
		{
			//transform a vector into the correct hrtf direction
			//fetch that direction and stuff from the hrtf stuff?
			//
		}

        IntPtr binauralRenderer = IntPtr.Zero;
    }
}