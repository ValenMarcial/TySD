// Client side implementation of UDP client-server model 
#include <stdio.h> 
#include <stdlib.h> 
#include <unistd.h> 
#include <string.h> 
#include <sys/types.h> 
#include <sys/socket.h> 
#include <arpa/inet.h> 
#include <netinet/in.h> 
#include <netdb.h>

#define SERVERPORT	8081 
#define MAXLINE     1024 
#define SERVERIP    "127.0.0.1"
#define SERVERNAME  "localhost"

// Driver code 
int main() { 
	int sockfd; 
	char buffer[MAXLINE]; 
	char *hello = "Hello from client"; 
	struct sockaddr_in servaddr;
    struct hostent *hostinfo;
	int n; 
    unsigned int len;

	// Creating socket file descriptor 
	if ( (sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0 ) { 
		perror("socket creation failed"); 
		exit(EXIT_FAILURE); 
	} 

	memset(&servaddr, 0, sizeof(servaddr)); 
	
	// Filling server information 
    servaddr.sin_family = AF_INET; 
	servaddr.sin_port = htons(SERVERPORT);
    servaddr.sin_addr.s_addr = inet_addr(SERVERIP);

    /*
    hostinfo = gethostbyname (SERVERNAME);
    if (hostinfo == NULL)
    {
      perror("Unknown host\n");
      exit (EXIT_FAILURE);
    }
    servaddr.sin_addr = *(struct in_addr *) hostinfo->h_addr;
    */

	sendto(sockfd, hello, strlen(hello), 0,(const struct sockaddr *) &servaddr,
           sizeof(servaddr)); 
	printf("Hello message sent.\n"); 
		
	n = recvfrom(sockfd, buffer, MAXLINE, MSG_WAITALL, 
                 (struct sockaddr*)&servaddr, &len); 
	buffer[n] = '\0'; 
	printf("Server response: %s\n", buffer); 

	close(sockfd); 
	return 0; 
} 

