# Matrix Reloaded
We are developing a peer to peer matrix multiplication processor.

The problems addressed as part of this project is reducing the time required to calculate matrix multiplications as well as distributing the load over several servers without overloading a single server. Despite the fact that there is a lot of study on parallel processing and distributed systems, parallelizing matrix multiplication using Strassen's approach is unique and there isn't much research done in this field. On top of that, we are solving various typical distributed system concerns such as fault tolerance, security, load balancing, availability, synchronization, and so on.

How to run-

PEER

To start the Peer-
1) First navigate to peer directory
2) Run "./final.sh X.X.X.X" - where X.X.X.X is ip address of server
3) Later run docker-compose up --build.

SERVER

To start the Server-
1) First navigate to server directory
2) Run docker-compose up --build.

Note :- To check the website url please run docker ps.
