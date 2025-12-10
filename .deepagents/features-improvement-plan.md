# Asteroids Game - Feature Improvement Plan

## Introdução

Este documento detalha o planejamento para implementar melhoramentos nas features do jogo Asteroids. Com base na análise do codebase atual, que inclui nave controlável, asteroides destrutíveis, sistema de vidas/pontuação e níveis progressivos, propomos 8 melhoramentos principais. Cada seção inclui descrição, benefícios, implementação detalhada, dependências e prioridade.

As melhorias visam manter o espírito clássico do jogo enquanto adicionam profundidade, replayability e polimento. Priorizamos features que aumentam o engajamento do jogador sem complicar excessivamente o código.

### Features Planejadas
1. Power-ups e Itens Coletáveis
2. Inimigos Adicionais (UFOs)
3. Efeitos Sonoros e Música
4. Efeitos Visuais Aprimorados
5. Sistema de High Scores
6. Menu Inicial e Pausa
7. Melhorias em Gameplay
8. Polimento Técnico

### Metodologia de Implementação
- Cada feature será implementada em branches separadas do Git.
- Testes manuais após cada implementação.
- Atualização de README.md e documentação conforme necessário.
- Uso de constantes em `constants.py` para novos valores configuráveis.

### Cronograma Estimado
- Fase 1 (Semanas 1-2): Power-ups, UFOs, Efeitos Visuais Básicos.
- Fase 2 (Semanas 3-4): Efeitos Sonoros, High Scores, Menu/Pausa.
- Fase 3 (Semana 5): Melhorias em Gameplay, Polimento Técnico.

## 1. Power-ups e Itens Coletáveis

### Descrição
Introduzir itens coletáveis que aparecem aleatoriamente ao destruir asteroides. Tipos: Escudo (protege contra 1 colisão), Velocidade (aumenta velocidade temporariamente), Multi-shot (tiros triplos por 10 segundos).

### Benefícios
- Aumenta replayability e estratégia.
- Dá ao jogador momentos de "vantagem" sem desbalancear.
- Incentiva destruição de asteroides.

### Implementação Detalhada
1. Criar classe `PowerUp` em `powerup.py`, herdando de `GameObject`.
   - Atributos: tipo, duração, posição.
   - Métodos: update (desaparece após tempo), draw (círculo colorido).
2. Adicionar constantes em `constants.py`:
   ```python
   POWERUP_TYPES = ['shield', 'speed', 'multishot']
   POWERUP_RADIUS = 10
   POWERUP_DURATION = 10.0  # seconds
   POWERUP_SPAWN_CHANCE = 0.2  # 20% chance per asteroid destroyed
   ```
3. Em `game.py`:
   - Lista `self.powerups = []`.
   - No `check_collisions`, após destruir asteroid, spawn powerup com chance.
   - Coleta: Verificar colisão player-powerup, aplicar efeito.
   - Atributos no Player: `self.shielded = False`, `self.speed_boost = 1.0`, `self.multishot = False`, `self.powerup_timer = 0`.
4. Modificar Player.update para aplicar boosts.
5. Draw powerups na tela.

### Dependências
- Classe GameObject existente.
- Modificações em Player e Game.

### Prioridade
Alta - Feature core que adiciona diversão imediata.

## 2. Inimigos Adicionais (UFOs)

### Descrição
UFOs que aparecem periodicamente, movem-se horizontalmente na tela, atiram projéteis aleatórios e dão pontos extras quando destruídos. Aparecem a partir do nível 3.

### Benefícios
- Aumenta desafio e variedade.
- Introduz elemento de "sobrevivência" além de asteroides.
- Pontos altos incentivam mira.

### Implementação Detalhada
1. Criar classe `UFO` em `ufo.py`, herdando de `GameObject`.
   - Movimento: Velocidade constante horizontal, wrap vertical.
   - Tiro: A cada 2-3 segundos, bullet em direção ao player (aproximada).
   - Pontuação: 200 pontos.
2. Constantes em `constants.py`:
   ```python
   UFO_RADIUS = 15
   UFO_SPEED = 100
   UFO_SHOOT_INTERVAL = 2.5
   UFO_SPAWN_LEVEL = 3
   UFO_SPAWN_CHANCE = 0.05  # per frame, adjusted for level
   ```
3. Em `game.py`:
   - Lista `self.ufos = []`.
   - Spawn: Em `update`, chance de spawn se nível >= UFO_SPAWN_LEVEL e poucos ufos ativos.
   - Colisões: Bullet vs UFO (similar a asteroid), Player vs UFO (perde vida).
   - Update e draw ufos.
4. Bullet do UFO: Usar classe Bullet existente, com velocidade reduzida.

### Dependências
- Classe Bullet e GameObject existentes.
- Modificações em Game para spawn e colisões.

### Prioridade
Alta - Adiciona inimigos dinâmicos, eleva dificuldade.

## 3. Efeitos Sonoros e Música

### Descrição
Adicionar sons para ações (tiro, explosão, thrust) e música de fundo arcade. Sons curtos em .wav, música em loop.

### Benefícios
- Imersão aumentada.
- Feedback auditivo para ações.
- Ambiente mais envolvente.

### Implementação Detalhada
1. Criar pasta `assets/sounds/` para arquivos de som.
2. Usar `pygame.mixer`:
   - Inicializar em `main.py`: `pygame.mixer.init()`.
   - Carregar sons em `constants.py` ou Game.__init__:
     ```python
     SOUND_SHOOT = pygame.mixer.Sound('assets/sounds/shoot.wav')
     SOUND_EXPLODE = pygame.mixer.Sound('assets/sounds/explode.wav')
     SOUND_THRUST = pygame.mixer.Sound('assets/sounds/thrust.wav')
     MUSIC_BACKGROUND = 'assets/sounds/background.mp3'
     ```
3. Reproduzir em eventos:
   - Tiro: No Player.shoot().
   - Explosão: No Game.check_collisions() após destruir asteroid/UFO.
   - Thrust: No Player.update() se thrusting (com flag para evitar loop).
   - Música: `pygame.mixer.music.load(MUSIC_BACKGROUND); pygame.mixer.music.play(-1)` no Game.__init__.
4. Volume ajustável: Adicionar constantes para volume.

### Dependências
- Arquivos de som (gratuitos ou criados).
- Pygame mixer.

### Prioridade
Média - Polimento importante, mas não essencial para gameplay.

## 4. Efeitos Visuais Aprimorados

### Descrição
Partículas para explosões, thrust melhorado, formas de asteroides variadas. Sistema de partículas para efeitos temporários.

### Benefícios
- Visual mais atrativo e moderno.
- Feedback visual claro para ações.
- Diferenciação visual entre entidades.

### Implementação Detalhada
1. Criar classe `Particle` em `particle.py`, herdando de `GameObject`.
   - Atributos: vida, cor, velocidade de fade.
   - Update: Diminuir vida, mover.
   - Draw: Círculo com alpha.
2. Explosões: No Game.check_collisions(), ao destruir, spawn 5-10 particles na posição.
3. Thrust: Modificar Player.draw() para particles atrás da nave quando thrusting.
4. Asteroides: Adicionar variações em _generate_shape() para cores diferentes (cinzas variadas).
5. Constantes:
   ```python
   PARTICLE_LIFETIME = 1.0
   PARTICLE_COUNT_EXPLODE = 8
   ```

### Dependências
- Classe GameObject.
- Modificações em draw de entidades.

### Prioridade
Média-Alta - Melhora apresentação sem mudar gameplay.

## 5. Sistema de High Scores

### Descrição
Salvar top 10 pontuações em arquivo JSON, com nomes. Tela de leaderboard no menu inicial.

### Benefícios
- Incentiva competição e replay.
- Feature padrão em jogos arcade.
- Persistência de progresso.

### Implementação Detalhada
1. Criar `highscores.py` com funções:
   - `load_highscores()`: Ler de 'highscores.json'.
   - `save_highscore(name, score)`: Inserir ordenado, salvar top 10.
   - `get_highscores()`: Retornar lista.
2. No Game.__init__, carregar highscores.
3. No game over, se score > menor highscore, pedir nome e salvar.
4. Menu: Estado separado para mostrar highscores.
5. Formato JSON: `[{'name': 'AAA', 'score': 1000}, ...]`.

### Dependências
- Biblioteca `json` (built-in).
- Estados de menu.

### Prioridade
Baixa-Média - Nice-to-have para completude.

## 6. Menu Inicial e Pausa

### Descrição
Menu inicial com opções: Start, High Scores, Quit. Pausa durante jogo com P, opções: Resume, Restart, Quit.

### Benefícios
- Experiência completa de jogo.
- Navegação profissional.
- Controle do jogador.

### Implementação Detalhada
1. Adicionar estados em Game: 'menu', 'playing', 'paused', 'highscores'.
2. Menu inicial: Desenhar botões, detectar clique/mouse.
   - Usar retângulos para botões, pygame.mouse para input.
3. Pausa: Tecla P alterna entre playing/paused.
   - Em paused, draw overlay com opções.
4. Transições: De menu para playing, paused para playing/restart/menu.
5. Draw separado para cada estado.

### Dependências
- Mouse input (pygame.mouse).
- Estados no loop principal.

### Prioridade
Média - Essencial para produto final polido.

## 7. Melhorias em Gameplay

### Descrição
Variedade em asteroides (cores diferentes, tipos especiais), upgrades (vida extra a cada 5 níveis), dificuldade ajustável.

### Benefícios
- Maior variedade e progresso.
- Adaptação ao nível do jogador.
- Extende duração do jogo.

### Implementação Detalhada
1. Asteroides variados: Em Asteroid.__init__, random type (normal, fast, armored - mais hits).
   - Adicionar hitpoints para armored.
2. Upgrades: A cada 5 níveis, +1 vida.
3. Dificuldade: Opção no menu para fácil/médio/difícil (menos vidas, mais asteroides).
4. Constantes: Adicionar para tipos de asteroid, upgrade thresholds.

### Dependências
- Modificações em Asteroid e Game.

### Prioridade
Baixa - Melhorias incrementais.

## 8. Polimento Técnico

### Descrição
Usar pygame.sprite.Group para entidades, refatorar Game em métodos menores, otimizar updates.

### Benefícios
- Melhor performance com muitos objetos.
- Código mais legível e manutenível.
- Preparação para expansão.

### Implementação Detalhada
1. Substituir listas por Groups: `self.asteroids = pygame.sprite.Group()`.
2. Refatorar Game.update: Separar em update_entities(), check_collisions(), etc.
3. Lazy loading de assets.
4. Profiling: Usar cProfile para identificar gargalos.

### Dependências
- pygame.sprite.
- Reestruturação de código.

### Prioridade
Baixa - Manutenção técnica.

## Conclusão

Este plano visa transformar o Asteroids de um jogo básico em uma experiência completa e polida, mantendo a simplicidade do original. As features foram priorizadas para maximizar impacto com esforço razoável. Comece pelas de alta prioridade para protótipo jogável, então adicione polimento.

### Próximos Passos
1. Criar branch para primeira feature (e.g., power-ups).
2. Implementar e testar incrementalmente.
3. Atualizar este documento conforme progresso.
4. Testes de usuário para balanceamento.

Para questões ou ajustes, consulte o codebase atual.

