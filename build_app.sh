git add .
git commit -m "CaesarAIEngineBackend online"
git push origin -f main:main
docker build -t palondomus/caesaraiengineworld:latest .
docker push palondomus/caesaraiengineworld:latest
docker run -it -p 8080:8080 palondomus/caesaraiengineworld:latest