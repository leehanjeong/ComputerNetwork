import java.io.*; 
import java.net.*; 

class TCPServerTh { 
	static public    Socket csocket;

  private static class MessageLoop implements Runnable {
	public void run() {
		String clientSentence; 
		String capitalizedSentence; 
		Socket connectionSocket;

		try {
		connectionSocket = csocket;
		BufferedReader inFromClient = 
              new BufferedReader(new
              InputStreamReader(connectionSocket.getInputStream())); 

 		DataOutputStream  outToClient = 
             new DataOutputStream(connectionSocket.getOutputStream()); 

		while(true) {
           clientSentence = inFromClient.readLine(); 
			if(clientSentence == null)
				break;
           if(clientSentence.length() == 0)
				break;

           capitalizedSentence = clientSentence.toUpperCase() + '\n'; 

           outToClient.writeBytes(capitalizedSentence); 
         }
		} catch (Exception e) {
        }
      }
  }

  public static void main(String argv[]) throws Exception 

    { 

      ServerSocket welcomeSocket = new ServerSocket(6789); 
  
      while(true) { 
  
            csocket = welcomeSocket.accept(); 

		Thread t = new Thread(new MessageLoop());
		t.start();
        } 

    } 

} 

