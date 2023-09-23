import json
import os
import requests
import asyncio
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, CallbackContext

# Substitua os valores abaixo pelos seus tokens e IDs
bot_token = os.getenv("TELEGRAM_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")
bot = Bot(token=bot_token)
# Definir os estados da conversa
PERIODO = range(1)

# Função para iniciar a conversa
def start(update: Update, context: CallbackContext) -> int:
    """
    Inicia a conversa com o usuário.

    Args:
        update: Objeto Update do Telegram.
        context: Objeto CallbackContext do Telegram.

    Returns:
        Número do estado da conversa.
    """

    update.message.reply_text(
        f"Olá! Este bot envia um relatório de CVEs encontrados nos últimos {PERIODO[0]} dias.\n"
        f"Para iniciar, escolha um período:"
    )

    return PERIODO

# Função para lidar com a escolha do período
def escolha_periodo(update: Update, context: CallbackContext) -> int:
    """
    Lida com a escolha do período pelo usuário.

    Args:
        update: Objeto Update do Telegram.
        context: Objeto CallbackContext do Telegram.

    Returns:
        Número do estado da conversa.
    """

    user_id = update.message.from_user.id
    periodos = {
        '1': 1,  # Último dia
        '2': 7,  # Últimos 7 dias
        '3': 15,  # Últimos 15 dias
        '4': 30  # Últimos 30 dias
    }

    # Obter a mensagem do usuário
    periodo_escolhido = update.message.text

    if periodo_escolhido not in periodos:
        update.message.reply_text("Por favor, escolha um período válido.")
        return PERIODO

    intervalo = periodos[periodo_escolhido]

    # Carregar o arquivo JSON correspondente ao intervalo escolhido
    file_path = f'dados_nist_{intervalo}_dias.json'
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Enviar os dados para o usuário
    for produto in data['products']:
        # Montar a mensagem
        mensagem = f"**CPE**: {produto['cpe']['cpeName']}\n" \
                   f"**Última Modificação**: {produto['cpe']['lastModified']}\n" \
                   f"**Título**: {produto['cpe']['titles'][0]['title']}\n" \
                   f"**Descontinuado**: {'Sim' if produto['cpe']['deprecated'] else 'Não'}\n" \
                   f"**Link do Produto**: [Link]({produto['cpe']['refs'][0]['ref']})\n" \
                   f"**Link do Change Log**: [Link]({produto['cpe']['refs'][1]['ref']})"

        # Enviar a mensagem para o Telegram
        bot.send_message(chat_id=chat_id, text=mensagem, parse_mode='MarkdownV2')

    update.message.reply_text(f"O relatório foi enviado com sucesso.")

    return ConversationHandler.END

async def main():
    updater = Updater(bot=bot, update_queue=True)
    dispatcher = await updater.initialize()

    # Adicionar handlers
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            PERIODO: [MessageHandler(None, escolha_periodo)],
        },
        fallbacks=[],
    )
    dispatcher.add_handler(conv_handler)

    # Iniciar o bot
    await updater.start_polling()
    await updater.idle()

if __name__ == '__main__':
    asyncio.run(main())