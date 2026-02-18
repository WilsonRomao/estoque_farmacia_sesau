import React from "react"

const MedicamentoList = ({Medicamento}) => {
    return < div>
        <h2>Medicamentos</h2>

        <table>
            <thead>
                <tr>
                    <th>Codigo do Medicamento</th>
                    <th>Nome do Medicamento</th>
                    <th>Quantidade</th>
                    <th>Ações</th>
                </tr>

            </thead>

            <tbody>
                {Medicamento.map((Medicamento) => (
                    <tr key={Medicamento.codigo_medicamento}>
                        <td>{Medicamento.nome_medicamento}</td>
                        <td>{Medicamento.quantidade}</td>
                        <td> 
                            <button>Update</button>
                            <button>Delete</button>
                        </td>
                    </tr>
                ))}
                
            </tbody>
        </table>
    
    </div>
}

export default MedicamentoList