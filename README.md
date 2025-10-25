# 🏛️ Arena de Gladiadores

Um jogo 2D no estilo *roguelike*, desenvolvido em **Python** com **Pygame Zero**, onde você controla um gladiador em batalhas dentro do Coliseu, enfrentando inimigos em fases desafiadoras até alcançar a vitória final.

---

## 🎮 Demonstração

O jogador controla um gladiador que deve **sobreviver e eliminar inimigos** que aparecem de diferentes portas do Coliseu.  
Cada fase tem um **número de inimigos a derrotar**. Após completar o objetivo, o jogador avança para a próxima fase.

---

## 🚀 Funcionalidades

- Sistema de **fases progressivas** (3 níveis de dificuldade)
- **IA inimiga** simples com movimentação e ataque automáticos  
- **Animações completas** (andar, atacar, ficar parado)  
- **Sistema de combate corpo a corpo**  
- **Gerenciamento de HP**, mortes e progresso  
- **Menus interativos**:  
  - Início  
  - Game Over  
  - Vitória  
- **Controle de som** (ligar/desligar)  
- **Arena circular** com zonas de entrada de inimigos  
- **Trilha sonora principal** (na pasta `music/`)  

---

## 🕹️ Controles

| Tecla | Ação |
|-------|------|
| ⬅️ / ➡️ | Mover para os lados |
| ⬆️ / ⬇️ | Mover para cima ou para baixo |
| **Espaço** | Atacar com espada |
| **Mouse** | Navegar nos menus |

---

## ⚙️ Instalação

1. **Clone o repositório ou extraia o ZIP:**
   ```bash
   git clone https://github.com/seu-usuario/ArenadeGladiadores.git
   cd roguelikegame
   ```

2. **Crie e ative um ambiente virtual (opcional, mas recomendado):**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate      # Windows
   ```

3. **Instale o Pygame Zero e o Pygame:**
   ```bash
   pip install pgzero pygame
   ```

4. **Execute o jogo:**
   ```bash
   pgzrun game.py
   ```

---

## 🧩 Estrutura do Projeto

```
roguelikegame/
│
├── game.py                  # Código principal do jogo
│
├── images/                  # Sprites e fundos
│   ├── idleright/
│   ├── idleleft/
│   ├── walkright/
│   ├── walkleft/
│   ├── attackright/
│   ├── attackleft/
│   └── cenario/
│
├── sounds/                  # Efeitos sonoros
│   ├── sword_slice.ogg
│   ├── young_man_being_hurt.ogg
│   
│
├── music/                   # Trilha sonora principal
│   └── somjogo.mp3
│
└── README.md                # Este arquivo
```

> ⚠️ As pastas `images`, `sounds` e `music` devem estar na mesma pasta que `game.py` para o jogo funcionar corretamente.

---

## 🧠 Tecnologias Utilizadas

- **Python 3.x**
- **Pygame Zero** (engine principal)
- **Pygame** (usado apenas para `Rect`)

---

## 🗺️ Mecânica do Jogo

- O jogador começa no **centro da arena** e enfrenta inimigos que entram por **portas aleatórias**.
- Cada inimigo possui **vida, dano e IA básica**, atacando quando está perto.
- Ao completar as **metas de abates de cada fase**, o jogador avança.
- Se o jogador perder toda a vida → **Game Over**.
- Ao vencer todas as fases → **Vitória!**

---


## 👨‍💻 Autor

**Fabio Ariel Vieira Bezerra**  
  
