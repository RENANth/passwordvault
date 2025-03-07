
# Gerenciador de Senhas Pessoal

Um aplicativo web seguro para armazenar e gerenciar suas senhas de forma criptografada, desenvolvido com Flask.

## Características

- **Segurança primeiro**: Todas as senhas são criptografadas usando AES via Fernet
- **Conta única**: Apenas um usuário é permitido por instância, tornando-o ideal para uso pessoal
- **Interface amigável**: Interface simples e intuitiva para gerenciar suas credenciais
- **Timeout de sessão**: Sessões expiram após 30 minutos de inatividade para maior segurança
- **Responsivo**: Funciona bem em dispositivos móveis e desktop

## Tecnologias utilizadas

- Flask - Framework web Python
- SQLAlchemy - ORM para interação com banco de dados
- SQLite - Banco de dados leve e portátil
- Cryptography - Biblioteca para criptografia segura
- Bootstrap - Framework CSS para interface responsiva

## Instalação e execução

### Pré-requisitos
- Python 3.11 ou superior

### Instalação
1. Clone este repositório:
```
git clone https://github.com/seu-usuario/gerenciador-senhas.git
cd gerenciador-senhas
```

2. Instale as dependências:
```
pip install -r requirements.txt
```

3. Configuração de variáveis de ambiente (opcional, mas recomendado para produção):
```
export SESSION_SECRET="sua_chave_secreta_para_sessao"
export ENCRYPTION_KEY="sua_chave_de_criptografia_de_32_bytes_base64"
```

4. Execute o aplicativo:
```
python main.py
```

5. Acesse `http://localhost:5000` no seu navegador

## Segurança

- A senha mestra é armazenada usando hashing seguro Werkzeug
- Todas as senhas salvas são criptografadas usando Fernet (AES-128)
- O sistema usa uma chave de desenvolvimento se nenhuma chave for fornecida através da variável de ambiente

## Atenção

Para uso em produção, certifique-se de configurar as variáveis de ambiente `SESSION_SECRET` e `ENCRYPTION_KEY` com valores seguros.

## Licença

Este projeto está licenciado sob a licença MIT.

## Contribuições

Contribuições, problemas e solicitações de recursos são bem-vindos!

## Sobre

Este projeto foi criado como um gerenciador de senhas pessoal seguro e simples de usar para aqueles que preferem manter suas senhas sob seu próprio controle em vez de confiar em serviços de terceiros.
