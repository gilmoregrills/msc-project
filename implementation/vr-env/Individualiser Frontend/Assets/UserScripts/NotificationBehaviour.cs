using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NotificationBehaviour : MonoBehaviour{
    GameObject attache;
    float theTime;

	// Use this for initialization
	void Start () {
        attache = this.gameObject;
        UnityEngine.Vector3 newPos = attache.transform.position;
        newPos.x = -15;
        newPos.y = -15;
        newPos.z = -15;
        attache.transform.position = newPos;
	}
	
	// Update is called once per frame
	void Update () {
        if (attache.transform.position.x >= -6)
        {
            if (theTime == 0)
            {
                theTime = Time.time;
            }
            else if (Time.time - theTime > 2)
            {
                UnityEngine.Vector3 newPos = attache.transform.position;
                newPos.x = -15;
                newPos.y = -15;
                newPos.z = -15;
                attache.transform.position = newPos;
                theTime = 0;
            }
            else
            {

            }
        }
    }
}
