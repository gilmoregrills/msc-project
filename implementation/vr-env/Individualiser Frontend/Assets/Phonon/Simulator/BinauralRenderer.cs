//
// Copyright 2017 Valve Corporation. All rights reserved. Subject to the following license:
// https://valvesoftware.github.io/steam-audio/license.html
//

using System;
using System.IO;
using System.Net.Sockets;
using System.Runtime.InteropServices;


namespace Phonon
{
    public class BinauralRenderer
    {
        public void Create(Environment environment, RenderingSettings renderingSettings, GlobalContext globalContext)
        {
            HRTFParams hrtfParams = new HRTFParams
            {
                type = HRTFDatabaseType.Custom,
                hrtfData = IntPtr.Zero,
                numHrirSamples = 101,
                loadCallback = OnLoadHrtf,
                unloadCallback = onUnloadHrtf,
                lookupCallback = onLookupHrtf
            };

            var error = PhononCore.iplCreateBinauralRenderer(globalContext, renderingSettings, hrtfParams, ref binauralRenderer);
            if (error != Error.None)
                throw new Exception("Unable to create binaural renderer [" + error.ToString() + "]");
        }

        public void OnLoadHrtf(int numSamples, int numSpectrumSamples, FFTHelper fft, IntPtr data)
        {
            
            UnityEngine.Debug.Log("data pointer points to: "+data.ToString());
            //declaring variables in tighter scope
            double[][][][] fullHrtf;
            TcpClient clientSocket;
            NetworkStream serverStream;
            Int32 size;
            byte[] sizeData;
            string asString;
            System.Runtime.Serialization.Formatters.Binary.BinaryFormatter bf = new System.Runtime.Serialization.Formatters.Binary.BinaryFormatter();
            MemoryStream ms = new MemoryStream();

            sizeData = new byte[24];
            clientSocket = new System.Net.Sockets.TcpClient();
            clientSocket.Connect("35.176.144.147", 54679);

            if (clientSocket.Connected)
            {
                UnityEngine.Debug.Log("connection made");
            }
            serverStream = clientSocket.GetStream();
            serverStream.Read(sizeData, 0, 24);
            asString = System.Text.Encoding.Default.GetString(sizeData);
            size = Int32.Parse(asString);
            UnityEngine.Debug.Log("size value = " + size);


            clientSocket.ReceiveTimeout = 1000;
            serverStream.ReadTimeout = 1000;
            StreamReader read = new StreamReader(serverStream);
            asString = read.ReadToEnd();
            UnityEngine.Debug.Log("end of hrtf as string \n" + asString.Substring(5540000));
            fullHrtf = Newtonsoft.Json.JsonConvert.DeserializeObject<double[][][][]>(asString);

            bf.Serialize(ms, fullHrtf);
            byte[] biter = ms.ToArray();
            //MOVE THIS HRTF DATA INTO THE INTPTR PROVIDED
            //Marshal.Copy(biter, 0, data, biter.Length);
            UnityEngine.Debug.Log("HRTFs loaded");
        }

        public void onUnloadHrtf()
        {
            UnityEngine.Debug.Log("");
            UnityEngine.Debug.Log("unloading hrtf data");
            //remove everything from memory

            //DESTROY THE HRTFDATA INTPTR
            //this.leftEarHrtfs = null;
            //this.rightEarHrtfs = null;
        }

        public void onLookupHrtf(System.IntPtr direction, System.IntPtr leftHrtf, System.IntPtr rightHrtf)
        {
            BinauralRenderer currentRenderer = new BinauralRenderer();
            Marshal.PtrToStructure(binauralRenderer, currentRenderer);
            
            //ONCE I FIND HOW TO GET THE HrtfData IntPtr I can get its size with IntPtr.size and do this stuff below:
            //System.Runtime.Serialization.Formatters.Binary.BinaryFormatter bf = new System.Runtime.Serialization.Formatters.Binary.BinaryFormatter();
            //byte[] biter = new byte[size];
            //Marshal.Copy(HRTFData, biter, 0, size);
            //MemoryStream mms = new MemoryStream(biter);
            //double[][][][] fullHrtf = (double[][][][])bf.Deserialize(mms);
            double[] directions;
            UnityEngine.Debug.Log(GetBinauralRenderer());
            UnityEngine.Debug.Log("Fetching HRTF for direction");
            //GRAB HRTF DATA FROM THE HRTFDATA INTPTR AND USE IT THAT WAY OMFG
            UnityEngine.Debug.Log(direction.ToString());
            UnityEngine.Debug.Log(direction.GetType());
            directions = new double[3];
            Marshal.Copy(direction, directions, 0, directions.Length);
            //double x = directions[0];
            //double y = directions[1];
            //double z = directions[2];
            UnityEngine.Debug.Log(directions);
            //transform a vector into the correct hrtf direction
            //fetch that direction and stuff from the hrtf stuff?

            //test version is currently always fetching the same HRTF regardless of input direction
            //Debug.Log(leftEarHrtfs[0][0].Length);
            //Marshal.Copy(leftEarHrtfs[0][0], 0, leftHrtf, leftEarHrtfs[0][0].Length);
            //Marshal.Copy(rightEarHrtfs[0][0], 0, rightHrtf, rightEarHrtfs[0][0].Length);
            //Debug.Log(leftHrtf.ToString());
            //Debug.Log(rightHrtf.ToString());
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