//
// Copyright (C) Valve Corporation. All rights reserved.
//
using System;
using System.Net.Sockets;
using UnityEngine;
using SimpleJSON;

namespace Phonon
{
    public class BinauralRenderer
    {
		System.Net.Sockets.TcpClient clientSocket;
		NetworkStream serverStream;
		byte[] inputData;
		string asString;
		JSONNode asJson;
		float[,,] leftEarHrir = new float[25, 50, 200];
		JSONArray leftEarHrtf;
		float[,,] rightEarHrir = new float[25, 50, 200];
		JSONArray rightEarHrtf;
        

        public void Create(Environment environment, RenderingSettings renderingSettings, GlobalContext globalContext)
        {
            HRTFParams hrtfParams = new HRTFParams
            {
				//yoooo I can set custom HRTFS with this set 
				type = HRTFDatabaseType.Custom, //IPL_HRTFDATABASETYPE_CUSTOM
                hrtfData = IntPtr.Zero, //set to zero always apparently
                numHrirSamples = 200, //the number of samples in my custom hrirs
				//gotta implement these callbacks to be able to use custom hrtfs yo! 
				loadCallback = onLoadHrtf, //this should point to a function that loads/fft's hrtfs?
                unloadCallback = onUnloadHrtf, //called when renderer is destroyed
                lookupCallback = null//onLookupHrtf() //points to a function that finds the hrtf based on direction coordinates returning L/R hrtfs
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
            float[,,,] fullHrtf = Newtonsoft.Json.JsonConvert.DeserializeObject<float[,,,]>(asString);
            Debug.Log("dimensions of input hrtf: ");
            Debug.Log(fullHrtf.GetLength(0));
            Debug.Log(fullHrtf.GetLength(1));
            Debug.Log(fullHrtf.GetLength(2));
            Debug.Log(fullHrtf.GetLength(3));
        }
		public void onUnloadHrtf()
		{
			//takes L and R hrir arrays! basically deletes
			//them from memory!!
		}

		void onLookupHrtf()
		{
			//transform a vector into the correct hrtf direction
			//fetch that direction and stuff from the hrtf stuff?
			//
		}

        IntPtr binauralRenderer = IntPtr.Zero;
    }
}