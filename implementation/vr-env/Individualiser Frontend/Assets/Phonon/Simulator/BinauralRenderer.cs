//
// Copyright (C) Valve Corporation. All rights reserved.
//
using System;
using System.Net.Sockets;
using System.Runtime.InteropServices;
using UnityEngine;

namespace Phonon
{
    public class BinauralRenderer
    {
		System.Net.Sockets.TcpClient clientSocket;
		NetworkStream serverStream;
		byte[] inputData;
		string asString;
		public double[][][] leftEarHrtfs;
		public double[][][] rightEarHrtfs;
        public double[][][][] fullHrtf;

        public void Create(Environment environment, RenderingSettings renderingSettings, GlobalContext globalContext)
        {
            HRTFParams hrtfParams = new HRTFParams
            {
				//yoooo I can set custom HRTFS with this set 
				type = HRTFDatabaseType.Default, //IPL_HRTFDATABASETYPE_CUSTOM
                hrtfData = IntPtr.Zero, //set to zero always apparently
                numHrirSamples = 202, //the number of samples in my custom hrirs
				//gotta implement these callbacks to be able to use custom hrtfs yo! 
				loadCallback = onLoadHrtf, //this should point to a function that loads/fft's hrtfs?
                unloadCallback = onUnloadHrtf, //called when renderer is destroyed - redundant basically with GC?
                lookupCallback = onLookupHrtf //points to a function that finds the hrtf based on direction coordinates returning L/R hrtfs
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

        public void onLoadHrtf(int numSamples, int numSpectrumSamples, Phonon.FFTHelper fft, System.IntPtr fftHelperData)
        {
            inputData = new byte[5545907];
            clientSocket = new System.Net.Sockets.TcpClient();
            clientSocket.Connect("127.0.0.1", 8080);
            if (clientSocket.Connected == true)
            {
                Debug.Log("connection made");
            }
            serverStream = clientSocket.GetStream();
            serverStream.Read(inputData, 0, inputData.Length);
            asString = System.Text.Encoding.Default.GetString(inputData);
            this.fullHrtf = Newtonsoft.Json.JsonConvert.DeserializeObject<double[][][][]>(asString);
            this.leftEarHrtfs = fullHrtf[0];
            this.rightEarHrtfs = fullHrtf[1];
            Debug.Log("hrtf length " + leftEarHrtfs[0][0].Length);
            Debug.Log("HRTFs loaded");
        }
		public void onUnloadHrtf()
		{
            Debug.Log("unloading hrtf data");
            //remove everything from memory
            Debug.Log(this.fullHrtf.Length);
            leftEarHrtfs = null;
            rightEarHrtfs = null;
        }

		public void onLookupHrtf(System.IntPtr direction, System.IntPtr leftHrtf, System.IntPtr rightHrtf)
		{
            Debug.Log("Fetching HRTF for direction");
            //transform a vector into the correct hrtf direction
            //fetch that direction and stuff from the hrtf stuff?

            //test version is currently always fetching the same HRTF regardless of input direction
            Debug.Log(leftEarHrtfs[0][0].Length);
            Marshal.Copy(leftEarHrtfs[0][0], 0, leftHrtf, leftEarHrtfs[0][0].Length);
            Marshal.Copy(rightEarHrtfs[0][0], 0, rightHrtf, rightEarHrtfs[0][0].Length);
            Debug.Log(leftHrtf.ToString());
            Debug.Log(rightHrtf.ToString());
		}

        IntPtr binauralRenderer = IntPtr.Zero;
    }
}