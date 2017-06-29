using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlaySample : MonoBehaviour {
	GameObject sourceObject;
	AudioSource audio;
	// Use this for initialization
	void Start () {
		sourceObject = GameObject.Find ("Source1");
		audio = sourceObject.GetComponent<AudioSource> ();
	}
	
	// Update is called once per frame
	void Update () {
		if (Input.GetKeyDown ("s") | Input.GetKeyDown ("left alt") && Input.GetKeyDown ("s")) {
			audio.PlayOneShot (audio.clip);
		}
	}
}
