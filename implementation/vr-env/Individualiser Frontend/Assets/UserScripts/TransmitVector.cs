using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net.Sockets;

public class TransmitVector : MonoBehaviour {
	
	Vector3 userToSource;
	Vector3 userLocalisation;
	GameObject user;
	GameObject source;
	GameObject reticle;
	System.Net.Sockets.TcpClient clientSocket;
	NetworkStream serverStream;
	byte[] output;

	// Use this for initialization
	void Start () {
		user = GameObject.Find("MegaCam");
		source = GameObject.Find("Source1");
		reticle = GameObject.Find("Ball");
	}
	
	// Update is called once per frame
	void Update () {
		if (Input.GetKeyDown ("x") | Input.GetKeyDown("left alt") && Input.GetKeyDown("x")) {
			print ("pressed X, transmitting perceived/actual source vector");
			userToSource = source.transform.position - user.transform.position;
			userLocalisation = reticle.transform.position - user.transform.position;
			print ("Actual vector from user to sound source =" + userToSource.ToString ());
			print ("Perceived vector from user to sound source =" + userLocalisation.ToString ());
			output = System.Text.Encoding.ASCII.GetBytes (userToSource.ToString () + userLocalisation.ToString ());
			clientSocket = new System.Net.Sockets.TcpClient ();
			clientSocket.Connect ("127.0.0.1", 8881);
			serverStream = clientSocket.GetStream ();
			serverStream.Write (output, 0, output.Length);
			serverStream.Flush ();
		}
			//calculate the current vector, send
			//that information to listening socket
			//in the individualiser module
	}
}
