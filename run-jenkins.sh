docker build -t jenkins-docker ./jenkins
docker rm -f jenkins
MSYS_NO_PATHCONV=1 docker run -d -u root --name jenkins --network cicd-net -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home -v /var/run/docker.sock:/var/run/docker.sock jenkins-docker