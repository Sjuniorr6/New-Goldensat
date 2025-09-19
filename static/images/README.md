# Imagens do Sistema

## Logo do Header

Para usar a imagem do logo no header do sistema:

1. **Salve a imagem do logo** com o nome `logo.png` nesta pasta (`static/images/`)
2. **Formato recomendado:** PNG com fundo transparente
3. **Tamanho recomendado:** 40x40 pixels (será redimensionado automaticamente)
4. **Qualidade:** Alta resolução para melhor visualização

## Logo de Fundo

Para usar a imagem do logo como fundo do sistema:

1. **Salve a imagem do logo** com o nome `logo-bg.png` nesta pasta (`static/images/`)
2. **Formato recomendado:** PNG com fundo transparente
3. **Tamanho recomendado:** 300x300 pixels ou maior
4. **Qualidade:** Alta resolução para melhor visualização

## Configuração Atual

### Logo do Header:
- **Tamanho:** 40x40 pixels (desktop), responsivo em mobile
- **Posição:** Lado esquerdo do header
- **Texto:** "Sistema" ao lado do logo
- **Cor:** Dourado (#d4af37)

### Logo de Fundo:
- **Tamanho:** 300x300 pixels
- **Posição:** Centro da tela
- **Repetição:** Não repetir
- **Anexo:** Fixo (não rola com o conteúdo)
- **Modo de mistura:** Overlay
- **Transparência:** 85% de opacidade do fundo

## Personalização

Para alterar a configuração do fundo, edite o arquivo `static/css/home.css` na seção `body` e `@media (prefers-color-scheme: dark)`.

### Opções disponíveis:
- `background-size`: Tamanho da imagem
- `background-position`: Posição da imagem
- `background-repeat`: Repetição da imagem
- `background-attachment`: Comportamento ao rolar
- `background-blend-mode`: Modo de mistura com o fundo
