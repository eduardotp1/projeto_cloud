# Projeto Final de CLoud
O objetivo do projeto foi implementar um load balancer com uma aplicação stateless.

### Como inicializar
Para rodar o projeto basta rodar o script abaixo, localizada dentro da pasta apos fazer o git clone deste repositorio:
```
./init.sh
```
Certifique que o arquivo tem as devidas permissoes.
Precisa completar o arquivo ```load.json``` com suas credenciais da AWS e quantidade de instancias que deseja manter rodando.
Espere um pouco para as maquinas subirem. 
Minha aplicação é um multiplicador, porém, com mais algumas modificações poderia se tornar uma calculadora, e trabalhando um pouco na aplicação, conseguimos ter um resultado muito bom. 
Para testar o multiplicador, basta rodar a linha abaixo, com o sendo o primeiro e segundo argumento os numeros a serem multiplicados.
```
python3 tarefa.py arg1 arg2
```
Ou pode acessar no browser a URL:
```
http://0.0.0.0:5000
````
```
http://0.0.0.0:5000/Multiplicador/<arg1>/<arg2>
````
Substituir arg1 e arg2 pelos numeros que deseja multiplicar

### Limpando instancias AWS
Rode o script abaixo:
```
python3 clean.py
```
