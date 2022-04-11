all : cli srv clo srvo clu srvu javap
cli : client.c
	gcc -g -o cli -Wall client.c
srv : server.c
	gcc -g -o srv -Wall server.c
clo : clientorg.c
	gcc -g -o clo -Wall clientorg.c
srvo : serverorg.c
	gcc -g -o srvo -Wall serverorg.c
clu : udpcli.c
	gcc -g -o clu -Wall udpcli.c
srvu : udpserver.c
	gcc -g -o srvu -Wall udpserver.c
javap : *.java
	javac *.java
clean :
	rm -rf *.exe  *.o *.class
