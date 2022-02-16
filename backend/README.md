How to deploy update
1. docker build . -t sportal:vx.x
2. docker tag sportal:vx.x registry.digitalocean.com/sportal-registry/sportal:vx.x
3. docker push registry.digitalocean.com/sportal-registry/sportal:vx.x
4. update image version in manifest.yaml
5. kubectl apply -f manifest.yaml

useful k8s commands:
kubectl get pods
kubectl get services
kubectl describe pod sportal-app


How to collect static
run latest docker image
1. docker run -it -p 8000:8000 sportal:vx.x /bin/bash
2. run 'python manage.py collectstatic'

How to add sport to parser
1. each league parser must fulfill the interface of getMatchesForTwoDays, getMatchesById, parseToMatch
2. add league to addEventTrigger
3. register league in admin portal
4. add parser to matchToParsers dictionary in parserUtils
if requiring a custom parser
5. add custom backend parser match controllers
6. add lid to matchLoader dictionary
