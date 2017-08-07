using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net.Sockets;


public class TransmitVector : MonoBehaviour {
	
	Vector3 userToSource;
	Vector3 userLocalisation;
    Vector3 newPosition;
    Vector3 currentPosition;
    Vector3[] potentialPositions;
    Quaternion currentRotation;
    Transform currentTransform;
    Transform newTransform;
    GameObject user;
	GameObject source;
	GameObject reticle;
    GameObject connectNotif;
    GameObject dataNotif;
    GameObject finishCube;
	System.Net.Sockets.TcpClient clientSocket;
	NetworkStream serverStream;
	byte[] output;
    int[] timesTested;
    System.Random rando;
    int[] positionCounter;

    // Use this for initialization
    void Start () {
        timesTested = new int[12];
        rando = new System.Random();
        user = GameObject.Find("MegaCam");
		source = GameObject.Find("Source1");
		reticle = GameObject.Find("Reticle");
        connectNotif = GameObject.Find("Connected");
        dataNotif = GameObject.Find("Sent Position");
        finishCube = GameObject.Find("CubeFinish");
        potentialPositions = new Vector3[8];

        potentialPositions[0] = new Vector3((float)-5.75, (float)5.75, (float)5.75);// up front left
        potentialPositions[1] = new Vector3((float)5.75, (float)5.75, (float)5.75);// up front right
        potentialPositions[2] = new Vector3((float)-5.75, (float)5.75, (float)-5.75);// up back left
        potentialPositions[3] = new Vector3((float)5.75, (float)5.75, (float)-5.75);// up back right

        potentialPositions[4] = new Vector3((float)-5.75, (float)-5.75, (float)5.75);// down front left
        potentialPositions[5] = new Vector3((float)5.75, (float)-5.75, (float)5.75);// down front right
        potentialPositions[6] = new Vector3((float)-5.75, (float)-5.75, (float)-5.75);// down back left
        potentialPositions[7] = new Vector3((float)5.75, (float)-5.75, (float)-5.75);// down back right

        //potentialPositions[8] = new Vector3(0, 0, 10);// front
        //potentialPositions[9] = new Vector3(0, 0, -10);// back
        //potentialPositions[10] = new Vector3(-10, 0, 0);// left
        //potentialPositions[11] = new Vector3(10, 0, 0);// right

        positionCounter = new int[12];
    }

    // Update is called once per frame
    void Update() {
        if (Input.GetKeyDown("x") | Input.GetKeyDown("left alt") && Input.GetKeyDown("x") | GvrController.AppButtonDown | GvrController.ClickButtonDown)
        {
            transmit();
        }
    }
    public void transmit() {
        //find all the game objects
        user = GameObject.Find("MegaCam");
        source = GameObject.Find("Source1");
        reticle = GameObject.Find("Reticle");
        connectNotif = GameObject.Find("Connected");
        dataNotif = GameObject.Find("Sent Position");
        //starting the script
        print ("pressed trigger, transmitting perceived/actual source vector");
        //fetch the current position values
		userToSource = source.transform.position - user.transform.position;
		userLocalisation = reticle.transform.position - user.transform.position;
        print ("Actual vector from user to sound source =" + userToSource.ToString ());
		print ("Perceived vector from user to sound source =" + userLocalisation.ToString ());

        //generate a new position for the sound source
        print("generating new random position");
        currentPosition = source.transform.position;
        currentRotation = source.transform.rotation;
        if (System.Array.IndexOf(positionCounter, 5) != -1 | System.Array.IndexOf(positionCounter, 4) != -1 | System.Array.IndexOf(positionCounter, 3) != -1 | System.Array.IndexOf(positionCounter, 2) != -1 | System.Array.IndexOf(positionCounter, 2) != -1 | System.Array.IndexOf(positionCounter, 1) != -1 | System.Array.IndexOf(positionCounter, 0) != -1)
        {
            int n = rando.Next(0, potentialPositions.Length);
            while (positionCounter[n] >= 6)
            {
                n = rando.Next(0, potentialPositions.Length);
            }
            positionCounter[n] = positionCounter[n] + 1;
            source.transform.SetPositionAndRotation(potentialPositions[n], currentRotation);
            Debug.Log(positionCounter[n]);
        } 
        else
        {
            //make some visual indicator appear
            Debug.Log("we're fucking done mate");
            finishCube.transform.SetPositionAndRotation(new Vector3(0, 0, 8), currentRotation);

        }
        //POTENTIALLY USE TIMESTESTED TO LIMIT THE NUMBER OF TIMES EACH SOURCE IS USED
        /*
        source.transform.SetPositionAndRotation((Random.insideUnitSphere.normalized * 10), currentRotation);
        while (source.transform.position.y < -5)
        {
            source.transform.SetPositionAndRotation((Random.insideUnitSphere.normalized * 10), currentRotation);
        }
        */
        source.transform.LookAt(new Vector3(0, 0, 0));
        print("new position = " + source.transform.position);
        newPosition = source.transform.position;

        //turn these directsions into strings to transmit them
        output = System.Text.Encoding.ASCII.GetBytes (userToSource.ToString () + userLocalisation.ToString () + newPosition.ToString());
        //start a TCP client
		clientSocket = new System.Net.Sockets.TcpClient ();
        clientSocket.Connect("35.176.144.147", 54678); //connect it to AWS instance
        //if connected flash the confirmation on-screen for a few seconds
        if (clientSocket.Connected)
        {
            connectNotif = GameObject.Find("Connected");
            UnityEngine.Vector3 pos = connectNotif.transform.position;
            pos.x = 1;
            pos.y = 1;
            pos.z = 7;
            connectNotif.transform.position = pos;
        }
		serverStream = clientSocket.GetStream ();
		serverStream.Write (output, 0, output.Length);
		serverStream.Flush ();
	}
}
