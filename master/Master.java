//Master component of the diffuse server
//Runs on some host and doles out connections to nodes

import java.net.*;
import java.io.*;

public class Master {
	//Define dynamic variables which will be reused
	private static Socket server;
	private static BufferedReader inPtr;
	private static OutputStream outPtr;

	private static void send(String msg) throws IOException {
		//Send a string on the open socket
		//String msg: string message to send

	    outPtr.write((msg+"\n").getBytes("UTF-8"));
	}

	private static String recv() throws IOException {
		//Receive a string on the open socket
		//return: String that was received

		String line = inPtr.readLine();
		String ret = "";
		while (!line.isEmpty()) {
			ret += line+'\n';
			line = inPtr.readLine();
		}

		return ret.substring(0,ret.length()-1);
	}

	public static void main(String[] args) throws Exception {
		int port = 1989;//Integer.parseInt(args[0]);

		//Start standard HTTP server loop and wait for requests

		ServerSocket serverSocket = new ServerSocket(port);
		//serverSocket.setSoTimeout(10000);

		String header = "HTTP/1.1 200 OK\r\n\r";

		while (true) {
			server = serverSocket.accept();
			System.out.println("Connection from "+server.getRemoteSocketAddress());

			//Set up streams for reading and writing
			inPtr = new BufferedReader(new InputStreamReader(server.getInputStream()));
			outPtr = server.getOutputStream();

			//Check the incoming connection
			String request = recv();
			System.out.println("Received initial request...");

			//If it is a server node...
			if (request == "NEW_NODE") {
				send();
			}
			//If it is an HTTP request from a browser...

			System.out.println("Sending message...");
			String msg = "<h1>THIS IS STUFF</h1>";
			System.out.println(msg+"--->");
			send(msg);

			System.out.println("Closing the socket...");
			inPtr.close();
			server.close();
		}
	}
}
