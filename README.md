Markdown

# 🌿 Jungle Shooter Adventure

Um jogo de plataforma e ação 2D desenvolvido em **Python** utilizando a biblioteca **Pygame Zero**. O objetivo é controlar o herói, desviar dos projéteis inimigos e alcançar o topo da fase através de desafios de plataforma.

## 🎮 Funcionalidades

* **Mecânicas de Plataforma:** Sistema de física personalizado com gravidade, colisão e pulo ajustado.
* **Inimigos com IA:** Inimigos patrulham as plataformas e disparam projéteis periodicamente na direção do jogador.
* **Animação de Sprites:** O herói e os inimigos possuem animações de "Idle" (parado) e "Walk" (andando), além de espelhamento (flip) automático dependendo da direção.
* **Sistema de Áudio:** Trilha sonora de fundo com botão de Mute/Unmute e efeitos sonoros de pulo.
* **Level Design:** Fase estruturada com múltiplas rotas, plataformas flutuantes e um objetivo final (Vitória).
* **Estados de Jogo:** Gerenciamento de telas de Menu, Gameplay, Game Over e Vitória.

## 🚀 Tecnologias Utilizadas

* **Python 3.11+**
* **Pygame Zero (pgzero)**
* **Pygame** (para manipulação avançada de Rects e Transform)

## 📂 Estrutura do Projeto

```text
JungleShooter/
├── images/        # Sprites do personagem, inimigos e tiles (Assets: Kenney)
├── sounds/        # Efeitos sonoros (.ogg/.wav)
├── music/         # Música de fundo
├── main.py        # Código fonte principal
└── README.md      # Documentação do projeto
🔧 Como Executar
Clone o repositório:

Bash

git clone [https://github.com/SEU_USUARIO/NOME_DO_REPO.git](https://github.com/SEU_USUARIO/NOME_DO_REPO.git)
Instale as dependências:

Bash

pip install pgzero
Execute o jogo:

Bash

pgzrun main.py
🎨 Créditos e Assets
Arte: Kenney Assets (Pixel Platformer).

Música: Pixabay (Royalty Free Music).

Código: Desenvolvido por Guilherme Santos.

Este projeto foi desenvolvido para fins de estudo sobre lógica de programação e desenvolvimento de jogos.
