# csm-reqauth-test-01
testing some aspects of requestAuthorization using service entries w JWTs

this requires a CSM-enabled GKE cluster set to your kube context

### set your project to envvar

```
export project=e2m-private-test-01 # replace with your project name
```

### setup ingress gateway 

in this case, we're just going to use a standard ingress gateway with external NLB

```
kubectl create namespace ingress-gateway
kubectl label namespace ingress-gateway istio-injection=enabled

kubectl -n ingress-gateway apply -k ingress-gateway/base
kubectl -n ingress-gateway apply -f gateway/
```

### setup demo app

```
kubectl create namespace whereami
kubectl label namespace whereami istio-injection=enabled

kubectl -n whereami apply -k whereami/variant
kubectl -n whereami apply -f whereami-vs/
```

### test endpoint

```
# get ingress gateway public IP
INGRESS_GATEWAY_IP=$(kubectl get service asm-ingressgateway -n ingress-gateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

# call the workload 
curl -s -H "Host: whereami.mesh.example.com" http://$INGRESS_GATEWAY_IP/ | jq
```

Now that this works, we can start setting up a simple JWKS endpoint using Cloud Run

### testing

```
# https://jwks-service.dchiesa.demo.altostrat.com/.well-known/jwks.json

kubectl apply -f requestAuth/
kubectl apply -f serviceEntry/

TOKEN=$(curl https://jwks-service.dchiesa.demo.altostrat.com/token -s -H 'Content-Type: application/json' -d '{"alg": "RS256","expiry": "3600s"}')
curl -s -H "Host: whereami.mesh.example.com" -H "Authorization: Bearer ${TOKEN}" http://$INGRESS_GATEWAY_IP/


```


