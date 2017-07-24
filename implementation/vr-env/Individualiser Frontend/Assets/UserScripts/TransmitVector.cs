using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net.Sockets;

public class TransmitVector : MonoBehaviour {
	
	Vector3 userToSource;
	Vector3 userLocalisation;
    Vector3 newPosition;
    Vector3 currentPosition;
    Quaternion currentRotation;
    Transform currentTransform;
    Transform newTransform;
    GameObject user;
	GameObject source;
	GameObject reticle;
    GameObject connectNotif;
    GameObject dataNotif;
	System.Net.Sockets.TcpClient clientSocket;
	NetworkStream serverStream;
	byte[] output;

	// Use this for initialization
	void Start () {
		user = GameObject.Find("MegaCam");
		source = GameObject.Find("Source1");
		reticle = GameObject.Find("Ball");
        connectNotif = GameObject.Find("Connected");
        dataNotif = GameObject.Find("Sent Position");
	}
	
	// Update is called once per frame
	void Update () {
		if (Input.GetKeyDown ("x") | Input.GetKeyDown("left alt") && Input.GetKeyDown("x")) {
			print ("pressed X, transmitting perceived/actual source vector");
			userToSource = source.transform.position - user.transform.position;
			userLocalisation = reticle.transform.position - user.transform.position;
            
            print ("Actual vector from user to sound source =" + userToSource.ToString ());
			print ("Perceived vector from user to sound source =" + userLocalisation.ToString ());

            print("generating new random position");
            currentPosition = source.transform.position;
            currentRotation = source.transform.rotation;
            source.transform.SetPositionAndRotation((Random.insideUnitSphere.normalized * 10), currentRotation);
            while (source.transform.position.y < -5)
            {
                source.transform.SetPositionAndRotation((Random.insideUnitSphere.normalized * 10), currentRotation);
            }
            source.transform.LookAt(new Vector3(0, 0, 0));
            print("new position = " + source.transform.position);
            newPosition = source.transform.position;
            output = System.Text.Encoding.ASCII.GetBytes (userToSource.ToString () + userLocalisation.ToString () + newPosition.ToString());
			clientSocket = new System.Net.Sockets.TcpClient ();
            
            clientSocket.Connect("35.176.144.147", 54678); //if running in editor, connect localhost
            
            if (clientSocket.Connected)
            {
                connectNotif = GameObject.Find("Connected");
                UnityEngine.Vector3 pos = connectNotif.transform.position;
                pos.x = -6;
                connectNotif.transform.position = pos;
            }

			serverStream = clientSocket.GetStream ();
			serverStream.Write (output, 0, output.Length);
            dataNotif.GetComponent<Renderer>().enabled = true;
			serverStream.Flush ();

		}
			//calculate the current vector, send
			//that information to listening socket
			//in the individualiser module
	}
}
