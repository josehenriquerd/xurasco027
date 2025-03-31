# Churrasco Calculator

Este projeto é uma calculadora de churrasco que estima a quantidade de carne, bebidas e outros itens necessários para um churrasco com base no número de adultos, crianças e tipo de evento.

![screencapture-127-0-0-1-5500-frontend-index-html-2025-03-31-20_15_51](https://github.com/user-attachments/assets/e9a4c042-aa1c-4411-b405-3cd18a0fd162)


## 🚀 Funcionalidades

- Cálculo automático da quantidade de carne por pessoa
- Estimativa de bebidas (cerveja, refrigerante e água)
- Escolha do tipo de churrasco (Completo, Hambúrguer, Pão de Alho, etc.)
- Cadastro de participantes
- Definição de quem será responsável por comprar os itens
- Interface interativa e responsiva

![screencapture-127-0-0-1-5500-frontend-index-html-2025-03-31-20_16_46](https://github.com/user-attachments/assets/d8b08f7e-f3d5-476c-b3af-d24989a3c859)


## 🛠 Tecnologias Utilizadas

- **Backend:** Python (Flask)
- **Frontend:** HTML, CSS e JavaScript
- **Banco de Dados:** (Opcional, pode ser adicionado no futuro)

## 📌 Como Rodar o Projeto

### 1️⃣ Instalar as dependências do Backend (Flask)

```bash
pip install -r requirements.txt
```

### 2️⃣ Rodar o Servidor Flask

```bash
python app.py
```

O backend estará disponível em `http://127.0.0.1:5000/`

### 3️⃣ Rodar o Frontend

Basta abrir o arquivo `index.html` em um navegador ou usar um servidor local como o Live Server do VSCode.

## 📡 Endpoints da API

### 🔹 `POST /calcular`

- **Descrição:** Calcula a quantidade necessária de carne, bebidas e custos do churrasco.
- **Parâmetros (JSON):**
  ```json
  {
      "adultos": 5,
      "criancas": 3,
      "tipo": "completo",
      "carne": 5,
      "bebidas": 4
  }
  ```
- **Resposta (JSON):**
  ```json
  {
      "total_carne_kg": 3.0,
      "cerveja_latas": 10,
      "refrigerante_litros": 4.0,
      "agua_litros": 3.2,
      "preco_total": 200.00,
      "carne_compradores": 5,
      "bebidas_compradores": 4
  }
  ```

## 🏗 Melhorias Futuras

- Cálculo Básico de Carne

  Bebidas e Acompanhamentos

  Carnes Variadas

  Orçamento Estimado

  Lista de Compras

  Quantidade de Carvão/Fogo

  Tempo de Preparo

  Modo Festa

  Compartilhar o Planejamento

  Perfil Alimentar dos Convidados

  Modo Econômico

  Clima e Localização

  Modo Churrasqueiro Experiente

  Calculadora de Sobras

  Integração com Supermercados

  Temporizador Interativo

  Modo Multi-Eventos

  Gamificação

  Modo Offline

  Modo Divisão de Custos

  Sugestão de Playlists

  Modo Churrasco Temático

  Registro de Feedback

  Simulador de Espaço

  Modo Crianças

  Alertas de Preparação

  Integração com Agenda

  Modo Churrasco ao Vivo
-

  📝 Contribuição

Sinta-se à vontade para abrir um pull request ou issue caso tenha sugestões ou melhorias!

## 📄 Licença

Este projeto está sob a licença MIT.

