
# Update package index and install prerequisites
```
sudo apt update && sudo apt upgrade -y
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
```
# Add Docker’s official GPG key
```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```
# Add Docker repository to sources
```
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
# Update package index again and install Docker
```
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io
```
# Start and enable Docker service
```
sudo systemctl start docker
sudo systemctl enable docker
```
# Add current user to Docker group to run Docker without sudo (optional)
```
sudo usermod -aG docker $USER
```
```
chmod 777 /var/run/docker.sock
```


# installation jenkins as docker container:
```
sudo docker run -p 8080:8080 -p 50000:50000 -d \
 -v jenkins_home:/var/jenkins_home \
 -v /var/run/docker.sock:/var/run/docker.sock \
 -v $(which docker):/usr/bin/docker jenkins/jenkins:lts
```

# view your container is up and running:
```
docker ps 
```
# to exec inside your container:
```
docker exec -it container-name bash
```


# to retrieve jenkins initation password 
```
docker exec -it container-name bash \
cat /var/jenkins_home/secrets/initialAdminPassword 
```
