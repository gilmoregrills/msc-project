using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TransmitVector : MonoBehaviour {
	
	Vector3 userToSource;
	Vector3 userLocalisation;
	GameObject user;
	GameObject source;
	GameObject reticle;

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
		}
			//calculate the current vector, send
			//that information to listening socket
			//in the individualiser module
	}
}
