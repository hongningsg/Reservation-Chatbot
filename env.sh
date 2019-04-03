docker build -t server_img server/.
docker build -t time_img timeService/.
docker build -t doc_img docService/.
docker network create --subnet=172.18.0.0/16 mynetwork
docker run -itd -p 127.0.0.1:9102:9102 --name server_C --network mynetwork --ip 172.18.0.3 server_img
docker run -itd -p 127.0.0.1:9101:9101 --name doc_C --network mynetwork --ip 172.18.0.2 doc_img
docker run -itd -p 127.0.0.1:9100:9100 --name time_C --network mynetwork --ip 172.18.0.4 time_img
