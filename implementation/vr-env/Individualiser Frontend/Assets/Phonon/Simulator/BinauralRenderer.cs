//
// Copyright (C) Valve Corporation. All rights reserved.
//
using System;
using System.Net.Sockets;
using System.Runtime.InteropServices;
using System.Text;
using UnityEngine;
using System.Collections;
namespace Phonon
{
    public class BinauralRenderer
    {
		System.Net.Sockets.TcpClient clientSocket;
		NetworkStream serverStream;
        Int32 size;
		byte[] inputData;
        byte[] sizeData;
		string asString;
		public double[][][] leftEarHrtfs;
		public double[][][] rightEarHrtfs;
        public double[][][][] fullHrtf;
        public double[] directions;
        GameObject connectNotif;
        GameObject fetchNotif;

        public void Create(Environment environment, RenderingSettings renderingSettings, GlobalContext globalContext)
        {
            HRTFParams hrtfParams = new HRTFParams
            {
				//yoooo I can set custom HRTFS with this set 
				type = HRTFDatabaseType.Custom, //IPL_HRTFDATABASETYPE_CUSTOM
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
            sizeData = new byte[24];
            clientSocket = new System.Net.Sockets.TcpClient();

            clientSocket.Connect("35.176.144.147", 54679); //if running in editor, connect localhost
            Debug.Log("connecting to local version");

            if (clientSocket.Connected)
            {
                Debug.Log("connection made");
                connectNotif = GameObject.Find("Connected");
                UnityEngine.Vector3 pos = connectNotif.transform.position;
                pos.x = 0;
                connectNotif.transform.position = pos;
            }
            serverStream = clientSocket.GetStream();
            serverStream.Read(sizeData, 0, 24);

            asString = System.Text.Encoding.Default.GetString(sizeData);

            size = Int32.Parse(asString);
            Debug.Log("size value = " + size);
            StringBuilder wip = new StringBuilder();
            inputData = new byte[1024];
            int numBytesRead = 0;
            clientSocket.ReceiveTimeout = 1000;
            serverStream.ReadTimeout = 1000;
            do
            {
                numBytesRead += serverStream.Read(inputData, 0, inputData.Length);

                wip.Append(System.Text.Encoding.Default.GetString(inputData));
                Debug.Log("bytes read: "+numBytesRead);

            } while (serverStream.DataAvailable);
            Debug.Log("bytes read: "+numBytesRead);

            asString = wip.ToString();
            Debug.Log("end of hrtf as string lol \n" + asString.Substring(5540000));
            int index = asString.IndexOf("]]]]") + 4;
            String doubles = asString.Substring(index);
            asString = asString.Substring(0, index);
            /*
            if (asString.Contains(doubles))
            {
                Debug.Log("they are doubles...");
                Debug.Log(doubles);
            }
            */
            //Debug.Log("hrtf as string lol \n" + asString.Substring(5540000));

            this.fullHrtf = Newtonsoft.Json.JsonConvert.DeserializeObject<double[][][][]>(asString);
            this.leftEarHrtfs = fullHrtf[0];
            this.rightEarHrtfs = fullHrtf[1];
            Debug.Log("hrtf shape: " + leftEarHrtfs.Length + ", " + leftEarHrtfs[0].Length + ", " + leftEarHrtfs[0][0].Length);
            Debug.Log("hrtf shape: " + rightEarHrtfs.Length + ", " + rightEarHrtfs[24].Length + ", " + rightEarHrtfs[24][49].Length);
            Debug.Log("HRTFs loaded");
            fetchNotif = GameObject.Find("Fetched HRTF");
            UnityEngine.Vector3 newPos = fetchNotif.transform.position;
            newPos.x = -6;
            fetchNotif.transform.position = newPos;
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
            Debug.Log(direction.ToString());
            Debug.Log(direction.GetType());
            this.directions = new double[3];
            Marshal.Copy(direction, directions, 0, directions.Length);
            //double x = directions[0];
            //double y = directions[1];
            //double z = directions[2];
            Debug.Log(directions);
            //transform a vector into the correct hrtf direction
            //fetch that direction and stuff from the hrtf stuff?

            //test version is currently always fetching the same HRTF regardless of input direction
            //Debug.Log(leftEarHrtfs[0][0].Length);
            //Marshal.Copy(leftEarHrtfs[0][0], 0, leftHrtf, leftEarHrtfs[0][0].Length);
            //Marshal.Copy(rightEarHrtfs[0][0], 0, rightHrtf, rightEarHrtfs[0][0].Length);
            //Debug.Log(leftHrtf.ToString());
            //Debug.Log(rightHrtf.ToString());
		}

        IntPtr binauralRenderer = IntPtr.Zero;
    }
}