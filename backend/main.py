# contem as rotas e endpoints
from flask import request, jsonify
from config import app,db
from models import Medicamento

import os

@app.route("/medicamento", methods=["GET"])
def get_medicamento():
    medicamento = Medicamento.query.all()
    json_medicamento = list(map(lambda x: x.to_json(), medicamento))
    return jsonify({"Medicamento":json_medicamento})

@app.route("/create_medicamento", methods =["POST"])
def create_medicamento():
    codigo_medicamento = request.json.get("codigoMedicamento")
    nome_medicamento = request.json.get("nomeMedicamento")
    quantidade = request.json.get("quantidade")


    if not codigo_medicamento or not nome_medicamento or not quantidade:
        return (
            jsonify({"message": "Você precisa inserir o codigo, nome e quantidade do medicamento"}),400,#Mensagem de erro
        )
    
    novo_medicamento = Medicamento(
        codigo_medicamento=codigo_medicamento,
        nome_medicamento=nome_medicamento,
        quantidade=quantidade
    )

    try: 
        db.session.add(novo_medicamento)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "message": str(e) #mensagem de erro
            }
        ),400
    
    return jsonify(
        {
            "message": "Medicamento criado" # Mensagem sucesso
        }
    ),201
    
@app.route("/update_medicamento/<string:codigo_medicamento>", methods=["PATCH"])
def update_content(codigo_medicamento):
    medicamento = Medicamento.query.get(codigo_medicamento)

    if not Medicamento:
        return jsonify(
            {
                "message": "Medicamento não encontrado" #mensagem de erro
            }
        ),404
    
    data = request.json
    medicamento.nome_medicamento = data.get("nomeMedicamento", medicamento.nome_medicamento)
    medicamento.quantidade = data.get("quantidade", medicamento.quantidade)

    db.session.commit()

    return jsonify(
        {
            "Message": "Medicamento atualizado"
        }
    )
    

@app.route("/delete_medicamento/<string:codigo_medicamento>", methods =["DELETE"])
def delete_medicamento(codigo_medicamento):
    medicamento = Medicamento.query.get(codigo_medicamento)

    if not Medicamento:
        return jsonify(
            {
                "message": "Medicamento não encontrado" #mensagem de erro
            }
        ),404
        
    db.session.delete(medicamento)
    db.session.commit()

    return jsonify({
        "message": "Medicamento deletado"
    })

@app.route("/upload", methods=["POST"])
def upload():
    # 1. Verifica se o arquivo está na requisição
    if 'file' not in request.files:
        return jsonify({"message": "Nenhum arquivo enviado"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"message": "Arquivo sem nome"}), 400

    # 2. Garante que a pasta existe (evita erro de 'Directory not found')
    upload_path = "uploads" # Recomendo usar um nome no plural
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)

    # 3. Salva o arquivo
    file.save(os.path.join(upload_path, file.filename))

    # 4. Retorna JSON em vez de Redirect
    # O React vai ler essa mensagem e mostrar o alert()
    return jsonify({"message": "Arquivo enviado com sucesso!"}), 201


#To run the aplication:
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)


