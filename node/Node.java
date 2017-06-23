import java.net.*;
import java.io.*;

public class Node {
	private static Socket client;
	private static BufferedReader inPtr;
	private static DataOutputStream outPtr;

	private static void send(String msg) throws IOException {
		//Send a string on the open socket
		//String msg: string message to send

		outPtr.writeUTF(msg+"\n\r\n");
	}

	private static String recv() throws IOException {
		//Receive a single newline delimited string on the open socket
		//return: String that was received

		return inPtr.readLine();
	}

	public static void main(String[] args) throws Exception {
		String serverName = args[0];
		int port = Integer.parseInt(args[1]);

		client = new Socket(serverName,port);
		System.out.println("Connected to "+serverName+":"+port+"\n");

		inPtr = new BufferedReader(new InputStreamReader(client.getInputStream()));
		outPtr = new DataOutputStream(client.getOutputStream());

		String msg = "Call";
		System.out.println("<---"+msg+"\n");
		send(msg);

		System.out.println("--->"+recv());

		client.close();
	}
}
