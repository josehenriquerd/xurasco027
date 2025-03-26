from flask import Flask, request, jsonify
from flask_cors import CORS
from flasgger import Swagger, swag_from

app = Flask(__name__)
CORS(app)
Swagger(app)

# Configurações
PRECOS_CARNE = {"picanha": 80, "frango": 20, "linguica": 30, "costela": 50}
PRECOS_ACOMPANHAMENTOS = {"arroz": 8, "farofa": 10, "vinagrete": 5, "pao_alho": 3}
TEMPOS_PREPARO = {"picanha": 40, "frango": 30, "linguica": 20, "costela": 120}
PRECOS_BEBIDAS = {"cerveja": 3, "refrigerante": 5, "agua": 2, "carvao": 5}
TODAS_CARNES = list(PRECOS_CARNE.keys())  # Lista de todas as carnes disponíveis

def calcular_carne(adultos, criancas, tipo, carnes, fator_reducao=1.0):
    base_adulto, base_crianca = 0.4, 0.2
    if tipo == "hamburguer":
        base_adulto, base_crianca = 0.2, 0.1
    elif tipo == "pao_alho":
        base_adulto, base_crianca = 0.1, 0.05

    total_carne_kg = 0
    preco_carne = 0
    for carne in carnes:
        carne_adultos = (adultos * base_adulto / len(carnes)) * fator_reducao
        carne_criancas = (criancas * base_crianca / len(carnes)) * fator_reducao
        total_carne_kg += carne_adultos + carne_criancas
        preco_carne += (carne_adultos + carne_criancas) * PRECOS_CARNE.get(carne, 50)
    return total_carne_kg, preco_carne

def calcular_bebidas(adultos, criancas, modo_festa, fator_reducao=1.0):
    multiplicador = 1.5 if modo_festa else 1
    cerveja = (adultos * 2 * multiplicador) * fator_reducao
    refrigerante = ((adultos * 0.5 + criancas * 0.7) * multiplicador) * fator_reducao
    agua = ((adultos * 0.4 + criancas * 0.5) * multiplicador) * fator_reducao
    preco_bebidas = (cerveja * PRECOS_BEBIDAS["cerveja"]) + (refrigerante * PRECOS_BEBIDAS["refrigerante"]) + (agua * PRECOS_BEBIDAS["agua"])
    return {"cerveja_latas": cerveja, "refrigerante_litros": refrigerante, "agua_litros": agua, "preco_bebidas": preco_bebidas}

def calcular_acompanhamentos(adultos, criancas, acompanhamentos, fator_reducao=1.0):
    quantidades = {
        "arroz": ((adultos * 0.1) + (criancas * 0.05)) * fator_reducao,
        "farofa": ((adultos * 0.08) + (criancas * 0.04)) * fator_reducao,
        "vinagrete": ((adultos * 0.05) + (criancas * 0.03)) * fator_reducao,
        "pao_alho": (adultos + (criancas * 0.5)) * fator_reducao
    }
    total_acompanhamentos = {k: quantidades[k] for k in acompanhamentos}
    preco_acompanhamentos = sum(quantidades[k] * PRECOS_ACOMPANHAMENTOS[k] for k in acompanhamentos)
    return total_acompanhamentos, preco_acompanhamentos

def calcular_carvao(total_carne_kg, fator_reducao=1.0):
    carvao_kg = (total_carne_kg * 1.2) * fator_reducao
    preco_carvao = carvao_kg * PRECOS_BEBIDAS["carvao"]
    return carvao_kg, preco_carvao

def calcular_tempo_preparo(carnes):
    return sum(TEMPOS_PREPARO.get(carne, 30) for carne in carnes) // len(carnes)

def calcular_divisao_custos(preco_total, pagantes):
    if pagantes <= 0:
        return 0
    return preco_total / pagantes

def ajustar_orcamento(preco_total, orcamento):
    if orcamento and preco_total > orcamento:
        return orcamento / preco_total
    return 1.0

@app.route('/calcular', methods=['POST'])
@swag_from({
    'tags': ['Churrasco'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'adultos': {'type': 'integer', 'example': 10},
                    'criancas': {'type': 'integer', 'example': 5},
                    'tipo': {'type': 'string', 'example': 'completo'},
                    'carnes': {'type': 'array', 'items': {'type': 'string'}, 'example': ['picanha', 'frango']},
                    'acompanhamentos': {'type': 'array', 'items': {'type': 'string'}, 'example': ['arroz', 'farofa']},
                    'modo_festa': {'type': 'boolean', 'example': False},
                    'pagantes': {'type': 'integer', 'example': 3},
                    'orcamento': {'type': 'number', 'example': 300}
                }
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Cálculo do churrasco',
            'schema': {
                'type': 'object',
                'properties': {
                    'total_carne_kg': {'type': 'number'},
                    'preco_carne': {'type': 'number'},
                    'bebidas': {'type': 'object'},
                    'acompanhamentos': {'type': 'object'},
                    'preco_acompanhamentos': {'type': 'number'},
                    'carvao_kg': {'type': 'number'},
                    'preco_carvao': {'type': 'number'},
                    'tempo_preparo': {'type': 'integer'},
                    'preco_total': {'type': 'number'},
                    'lista_compras': {'type': 'object'},
                    'custo_por_pessoa': {'type': 'number'},
                    'ajustado_orcamento': {'type': 'boolean'}
                }
            }
        },
        '400': {'description': 'Erro nos dados enviados'}
    }
})
def calcular():
    dados = request.get_json()
    adultos = dados.get('adultos', 0)
    criancas = dados.get('criancas', 0)
    tipo = dados.get('tipo', 'completo')
    carnes = dados.get('carnes', ['picanha'])
    acompanhamentos = dados.get('acompanhamentos', [])
    modo_festa = dados.get('modo_festa', False)
    pagantes = dados.get('pagantes', adultos)
    orcamento = dados.get('orcamento', None)

    if not isinstance(adultos, int) or not isinstance(criancas, int) or adultos < 0 or criancas < 0 or pagantes < 0:
        return jsonify({"error": "Valores inválidos"}), 400

    # Se for "completo", usar todas as carnes disponíveis
    if tipo == "completo":
        carnes = TODAS_CARNES

    # Primeiro cálculo sem ajuste
    total_carne_kg, preco_carne = calcular_carne(adultos, criancas, tipo, carnes)
    bebidas = calcular_bebidas(adultos, criancas, modo_festa)
    acompanhamentos, preco_acompanhamentos = calcular_acompanhamentos(adultos, criancas, acompanhamentos)
    carvao_kg, preco_carvao = calcular_carvao(total_carne_kg)
    preco_total = preco_carne + bebidas["preco_bebidas"] + preco_acompanhamentos + preco_carvao

    # Ajuste pelo orçamento
    fator_reducao = ajustar_orcamento(preco_total, orcamento)
    ajustado_orcamento = fator_reducao < 1.0

    # Recalcular com o fator de redução, se necessário
    if ajustado_orcamento:
        total_carne_kg, preco_carne = calcular_carne(adultos, criancas, tipo, carnes, fator_reducao)
        bebidas = calcular_bebidas(adultos, criancas, modo_festa, fator_reducao)
        acompanhamentos, preco_acompanhamentos = calcular_acompanhamentos(adultos, criancas, acompanhamentos, fator_reducao)
        carvao_kg, preco_carvao = calcular_carvao(total_carne_kg, fator_reducao)
        preco_total = preco_carne + bebidas["preco_bebidas"] + preco_acompanhamentos + preco_carvao

    custo_por_pessoa = calcular_divisao_custos(preco_total, pagantes)
    tempo_preparo = calcular_tempo_preparo(carnes)

    lista_compras = {
        "carnes": {carne: f"{total_carne_kg / len(carnes):.2f} kg" for carne in carnes},
        "bebidas": {k: f"{v:.1f}" for k, v in bebidas.items() if k != "preco_bebidas"},
        "acompanhamentos": {k: f"{v:.2f}" for k, v in acompanhamentos.items()},
        "carvao": f"{carvao_kg:.2f} kg"
    }

    return jsonify({
        "total_carne_kg": total_carne_kg,
        "preco_carne": preco_carne,
        "bebidas": bebidas,
        "acompanhamentos": acompanhamentos,
        "preco_acompanhamentos": preco_acompanhamentos,
        "carvao_kg": carvao_kg,
        "preco_carvao": preco_carvao,
        "tempo_preparo": tempo_preparo,
        "preco_total": preco_total,
        "lista_compras": lista_compras,
        "custo_por_pessoa": custo_por_pessoa,
        "ajustado_orcamento": ajustado_orcamento
    })

if __name__ == '__main__':
    app.run(debug=True)