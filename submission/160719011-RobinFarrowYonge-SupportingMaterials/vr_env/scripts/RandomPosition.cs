using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class RandomPosition : MonoBehaviour {
	GameObject audioSource;
	Vector3 currentPosition;
	Quaternion currentRotation;
	Transform currentTransform;
	Transform newTransform;
    GameObject positionNotif;
	// Use this for initialization
	void Start () {
		audioSource = GameObject.Find ("Source1");
		Random rnd = new Random ();
		audioSource.transform.SetPositionAndRotation((Random.insideUnitSphere.normalized * 10), currentRotation);
		audioSource.transform.LookAt (new Vector3 (0, 0, 0));
        positionNotif = GameObject.Find("New Position");
	}
	
	// Update is called once per frame
	void Update () {
		if (Input.GetKeyDown ("z") | Input.GetKeyDown("left alt") && Input.GetKeyDown("z")) {
			print ("generating new random position");
			currentPosition = audioSource.transform.position;
			currentRotation = audioSource.transform.rotation;
			print ("current position = " + currentPosition);
			audioSource.transform.SetPositionAndRotation((Random.insideUnitSphere.normalized * 10), currentRotation);
            positionNotif.GetComponent<Renderer>().enabled = true;
            while (audioSource.transform.position.y < -5) {
				audioSource.transform.SetPositionAndRotation((Random.insideUnitSphere.normalized * 10), currentRotation);
			}
			audioSource.transform.LookAt (new Vector3 (0, 0, 0));
            print("new position = " + audioSource.transform.position);
            //play audio sample
        }
    }
}