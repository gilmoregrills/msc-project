using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class RandomPosition : MonoBehaviour {
	GameObject audioSource;
	Vector3 currentPosition;
	Quaternion currentRotation;
	Transform transform;
	Transform newTransform;
	// Use this for initialization
	void Start () {
		audioSource = GameObject.Find ("Source1");
		Random rnd = new Random ();
		audioSource.transform.SetPositionAndRotation((Random.insideUnitSphere.normalized * 10), currentRotation);
		audioSource.transform.LookAt (new Vector3 (0, 0, 0));
	}
	
	// Update is called once per frame
	void Update () {
		if (Input.GetKeyDown ("z") | Input.GetKeyDown("left alt") && Input.GetKeyDown("z")) {
			print ("pressed Z - generating new random position");
			currentPosition = audioSource.transform.position;
			currentRotation = audioSource.transform.rotation;
			print ("current position = " + currentPosition);
			audioSource.transform.SetPositionAndRotation((Random.insideUnitSphere.normalized * 10), currentRotation);
			while (audioSource.transform.position.y < -5) {
				audioSource.transform.SetPositionAndRotation((Random.insideUnitSphere.normalized * 10), currentRotation);
			}
			audioSource.transform.LookAt (new Vector3 (0, 0, 0));
			//play audio sample
		}
	}
}