# api_verificar_licenca
This is an API to check license codes using Flask + MongoDB

# Pré Requisito:    

Ter instalado o MongoDB e o serviço estar ativo.    
Ref.:  https://www.mongodb.com/try/download/community    
    
# Usando o mongosh crie uma database com os comandos abaixo:    
use expert_advisor   
db.users.insertOne( { x: 1 } );    
show collections    
    
# insira o primeiro usuario para poder acessar o sistema com o comando abaixo:    
db.users.insertOne({"_id": 1, "name": "admin", "email": "admin@admin.db", "password": "123456","accounts": 27032026, "exp_month": 12, "exp_year": 2026});      
    
# Agora você já pode sair do monosh    
quit();    
    
# Para subir a API    
pip install -r requirements.txt

python main.py

# Abra a pagina da web de apoio / testes    
dentro da pasta www click em index.htm e preencha o campo e-mail e senha com os dados abaixo:    
email: admin@admin.db    
senha: 123456    
