#                               ------ ESTUDANTE *A* -------
from datetime import datetime

def validarData(dataStr, formato="%Y-%m-%d"):
    try:
        datetime.strptime(dataStr, formato)
        return True  
    except ValueError:
        return False  


contador_ids = {} 

def adicionarEvento(listaEventos, nome, data, local, categoria):
    if not nome.strip() or not data.strip() or not local.strip() or not categoria.strip():
        print("Aviso: todos os campos devem ser preenchidos.")
        return False
    
    if not validarData(data):
        print("Data inválida: por favor digite no formato AAAA-MM-DD")
        return False
    
    #verificaçao de duplicatas
    for evento in listaEventos:
        if (evento['nome'].lower().strip() == nome.lower().strip() and \
        evento['data'].strip() == data.strip() and \
        evento ['categoria'].lower().strip() == categoria.lower().strip()):
            print('Falha ao adicionar: evento já existe na lista.')
            return False
    
    
        
    #gera ID's baseados na Categoria
    global contador_ids 
    categoria_prefixo = categoria[:3].upper().strip()
   
    if categoria_prefixo not in contador_ids:
        contador_ids[categoria_prefixo] = 1
    else:
        contador_ids[categoria_prefixo] += 1

    novoID = f'{categoria_prefixo}-{contador_ids[categoria_prefixo]}'

    novoEvento = {
        'id' : novoID,
        'nome' : nome.strip(),
        'data' : data.strip(),
        'local' : local.strip(),
        'categoria' : categoria.strip(),
        'participado': False
    }

    listaEventos.append(novoEvento)
    print(f'Evento {nome} adicionado com sucesso! ')
    return True

def listarEventos(listaEventos):
    if not listaEventos:
        print('Lista de eventos vazia. Use a opção 1 para adicionar um evento')
        return False
    
    #converte o valor booleano de 'participado' em texto
    for evento in listaEventos:
        if evento['participado']: #True
            statusParticipacao = 'Sim'
        else:
            statusParticipacao = 'Não'

        print("\033[1;30m" + "-~~•─• Detalhes do Evento •─•~~-" + "\033[0m")
        print(f'ID: {evento["id"]}')
        print(f'Nome: {evento["nome"]}')
        print(f'Data: {evento["data"]}')
        print(f'Local: {evento["local"]}')
        print(f'Categoria: {evento["categoria"]}')
        print(f'Participado: {statusParticipacao}')

    return True


def procurarEventoPorNome(listaEventos, nome):
    nomes_encontrados = [] #lista temporaria para guardar os eventos encontrados
    contador = 0 

    for evento in listaEventos:
        if nome.lower() in evento['nome'].lower():
            nomes_encontrados.append(evento)
            contador += 1

    if contador == 0:
        print(f'Nenhum evento foi encontrado com o nome: {nome}')
    elif contador == 1:
        print(f'1 evento encontrado com o nome: {nome}')
    else:
        print(f'{contador} eventos foram encontrados com o nome: {nome}')

    if nomes_encontrados:
        listarEventos(nomes_encontrados) #mostra detalhadamente o(s) evento(s)
     
    return bool(nomes_encontrados)

def deletarEvento(listaEventos, id):
    for evento in listaEventos:
        if id == evento['id']:
            print(f'Tem certeza que deseja deletar esse evento: {evento['nome']} -> ID: {evento['id']}?')
            escolha = input('Digite "Sim" para continuar, ou digite "Não" para cancelar a operação: ')
            if escolha.strip().lower() == 'sim':
                listaEventos.remove(evento)
                print('O Evento foi removido com sucesso')
                return True 
            elif escolha.strip().lower() == 'nao' or 'não':
                print('A operação está sendo cancelada')
                return False
            else:
                print('Resposta inválida. Digite apenas "Sim" ou "Não"')
                return False     
    return False

    
# =============== ESTUDANTE B: INTERFACE E RELATÓRIOS ===============

def displayMenu():
    print("\n" + "="*50)
    print("           🎉 GERENCIADOR DE EVENTOS 🎉")
    print("="*50)
    print("1. ➕ Adicionar novo evento")
    print("2. 📋 Listar todos os eventos")
    print("3. 🔍 Buscar evento por nome")
    print("4. 🏷️  Filtrar eventos por categoria")
    print("5. ✅ Marcar evento como participado")
    print("6. 📊 Gerar relatório resumido")
    print("7. 🗑️  Excluir evento por ID")
    print("0. ❌ Sair")
    print("="*50)

def getEscolhaDoUsuario():
    try:
        return int(input("➡️  Escolha uma opção: "))
    except ValueError:
        return -1

def filtrarEventosPorCategoria(listaEventos, categoria):
    categoria = categoria.strip().lower()
    encontrados = [evento for evento in listaEventos if categoria in evento["categoria"].lower()]
    if encontrados:
        print(f"\n🏷️  Eventos na categoria '{categoria}':")
        for evento in encontrados:
            status = "✅ Participado" if evento.get("participado", False) else "❌ Não participado"
            print(f"ID: {evento['id']} | Nome: {evento['nome']} | Data: {evento['data']} | "
                  f"Local: {evento['local']} | {status}")
    else:
        print(f"Nenhum evento encontrado na categoria '{categoria}'.")
    return encontrados

def marcarEventoAtendido(listaEventos, id):
    for evento in listaEventos:
        if evento["id"] == id:
            evento["participado"] = True
            print(f"✅ Evento '{evento['nome']}' (ID: {id}) marcado como participado!")
            return True
    print(f"❌ Evento com ID {id} não encontrado.")
    return False

def gerarRelatorio(listaEventos):
    total = len(listaEventos)
    if total == 0:
        print("📊 Nenhum evento cadastrado para gerar relatório.")
        return

    categorias = {}
    participados = 0

    for evento in listaEventos:
        cat = evento["categoria"]
        categorias[cat] = categorias.get(cat, 0) + 1
        if evento.get("participado", False):
            participados += 1

    perc_participados = (participados / total) * 100 if total > 0 else 0

    print("\n" + "="*40)
    print("        📊 RELATÓRIO RESUMIDO")
    print("="*40)
    print(f"📌 Total de eventos: {total}")
    print(f"✅ Eventos participados: {participados} ({perc_participados:.1f}%)")
    print("\n📈 Eventos por categoria:")
    for cat, qtd in categorias.items():
        print(f"   • {cat}: {qtd}")
    print("="*40)

# =============== FUNÇÃO PRINCIPAL ===============

def main():
    eventos = []

    while True:
        displayMenu()
        escolha = getEscolhaDoUsuario()

        if escolha == 0:
            print("👋 Obrigado por usar o Gerenciador de Eventos! Até logo!")
            break

        elif escolha == 1:
            print("\n--- ➕ Adicionar Novo Evento ---")
            nome = input("Nome do evento: ").strip()
            data = input("Data (AAAA-MM-DD): ").strip()
            local = input("Local: ").strip()
            categoria = input("Categoria: ").strip()
            adicionarEvento(eventos, nome, data, local, categoria)

        elif escolha == 2:
            print("\n--- 📋 Lista de Todos os Eventos ---")
            listarEventos(eventos)

        elif escolha == 3:
            print("\n--- 🔍 Buscar Evento por Nome ---")
            nome_busca = input("Digite parte do nome: ")
            procurarEventoPorNome(eventos, nome_busca)

        elif escolha == 4:
            print("\n--- 🏷️  Filtrar por Categoria ---")
            cat_busca = input("Digite a categoria: ")
            filtrarEventosPorCategoria(eventos, cat_busca)

        elif escolha == 5:
            print("\n--- ✅ Marcar Evento como Participado ---")
            try:
                id_evento = int(input("ID do evento: "))
                marcarEventoAtendido(eventos, id_evento)
            except ValueError:
                print("❌ ID inválido. Digite um número inteiro.")

        elif escolha == 6:
            print("\n--- 📊 Gerar Relatório ---")
            gerarRelatorio(eventos)

        elif escolha == 7:
            print("\n--- 🗑️  Excluir Evento ---")
            try:
                id_evento = int(input("ID do evento: "))
                deletarEvento(eventos, id_evento)
            except ValueError:
                print("❌ ID inválido. Digite um número inteiro.")

        else:
            print("⚠️  Opção inválida. Tente novamente.")

        input("\nPressione ENTER para continuar...")

if __name__ == "__main__":
    main()