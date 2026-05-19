import flet as ft
import sqlite3

# --- GERENCIAMENTO DO BANCO DE DADOS OFFLINE ---
def inicializar_banco():
    # Cria o arquivo de banco de dados dentro do próprio telemóvel
    conn = sqlite3.connect("basa_dados.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conteudo TEXT NOT NULL
        )
    ''')
    conn.commit()
    return conn

def main(page: ft.Page):
    # Configurações iniciais da tela do aplicativo
    page.title = "MuchangaBasa"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.spacing = 15
    
    # Conecta ao banco local
    conexao = inicializar_banco()
    cursor = conexao.cursor()

    # Espaço visual onde as notas/tarefas vão aparecer empilhadas
    lista_tarefas = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)

    # Função que busca as notas salvas no telemóvel e desenha na tela
    def atualizar_lista():
        lista_tarefas.controls.clear()
        cursor.execute("SELECT conteudo FROM tarefas ORDER BY id DESC")
        for linha in cursor.fetchall():
            lista_tarefas.controls.add(
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color=ft.Colors.BLUE_700),
                        ft.Text(linha[0], size=16, color=ft.Colors.BLACK87, weight=ft.FontWeight.W_500)
                    ]),
                    padding=12,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=8,
                    shadow=ft.BoxShadow(blur_radius=2, color=ft.Colors.BLACK12)
                )
            )
        page.update()

    # Função para guardar o que foi digitado
    def salvar_tarefa(e):
        texto = entrada_texto.value.strip()
        if texto:
            cursor.execute("INSERT INTO tarefas (conteudo) VALUES (?)", (texto,))
            conexao.commit()
            entrada_texto.value = "" # Limpa a caixa de digitação
            atualizar_lista()

    # --- COMPONENTES VISUAIS DA INTERFACE ---
    
    # Cabeçalho Principal
    cabecalho = ft.Column([
        ft.Text("MuchangaBasa", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
        ft.Text("Gestor de Tarefas Académicas e Profissionais", size=14, color=ft.Colors.GREY_600)
    ], spacing=2)

    # Campo de texto para digitação
    entrada_texto = ft.TextField(
        hint_text="O que precisa organizar hoje? Digite aqui...",
        border_radius=8,
        bgcolor=ft.Colors.WHITE,
        content_padding=15
    )

    # Botão de salvar estilizado
    btn_salvar = ft.ElevatedButton(
        text="Guardar no Dispositivo",
        icon=ft.Icons.SAVE,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE_700,
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
        height=50,
        on_click=salvar_tarefa
    )

    # Monta a estrutura da tela adicionando os blocos criados
    page.add(
        cabecalho,
        entrada_texto,
        btn_salvar,
        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
        lista_tarefas
    )

    # Carrega os dados salvos assim que o usuário abre o app
    atualizar_lista()

# Inicializa o app
if __name__ == "__main__":
    ft.app(target=main)
