using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlaySample : MonoBehaviour {
	GameObject sourceObject;
	AudioSource audioSource;
	// Use this for initialization
	void Start () {
		sourceObject = GameObject.Find ("Source1");
		audioSource = sourceObject.GetComponent<AudioSource> ();
	}
	
	// Update is called once per frame
	void Update () {
		if (Input.GetKeyDown ("s") | Input.GetKeyDown ("left alt") && Input.GetKeyDown ("s")) {
            Debug.Log("playing sample");
			audioSource.PlayOneShot (audioSource.clip);
		}
	}
}
