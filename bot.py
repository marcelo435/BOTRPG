import discord
from discord.ext import commands
import random
import json
import os

# --- CONFIGURAÇÕES INICIAIS ---
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents)

# Arquivo para não perder os dados
NOME_ARQUIVO = "dados_rpg.json"

# Carregar dados salvos
if os.path.exists(NOME_ARQUIVO):
    with open(NOME_ARQUIVO, "r") as f:
        try:
            dados_brutos = json.load(f)
            # Converte chaves de string para int
            dados_rpg = {int(k): v for k, v in dados_brutos.items()}
        except:
            dados_rpg = {}
else:
    dados_rpg = {}

def salvar_dados():
    with open(NOME_ARQUIVO, "w") as f:
        json.dump(dados_rpg, f)

def garantir_usuario(user_id):
    # Se o usuário não existe, cria do zero
    if user_id not in dados_rpg:
        dados_rpg[user_id] = {"hp": 100, "pe": 20, "san": 100}
    
    # SE O DADO FOR ANTIGO (apenas int ou dict incompleto), atualiza
    if isinstance(dados_rpg[user_id], int):
        vida_antiga = dados_rpg[user_id]
        dados_rpg[user_id] = {"hp": vida_antiga, "pe": 20, "san": 100}
    
    # Garante que todas as chaves existem
    if "hp" not in dados_rpg[user_id]: dados_rpg[user_id]["hp"] = 100
    if "pe" not in dados_rpg[user_id]: dados_rpg[user_id]["pe"] = 20
    if "san" not in dados_rpg[user_id]: dados_rpg[user_id]["san"] = 100  # Valor padrão de Sanidade

# --- CLASSE PAINEL DE VIDA (HP) ---
class PainelVida(discord.ui.View):
    def __init__(self, alvo):
        super().__init__(timeout=None)
        self.alvo = alvo

    def gerar_barra(self):
        garantir_usuario(self.alvo.id)
        hp = dados_rpg[self.alvo.id]["hp"]
        pe = dados_rpg[self.alvo.id]["pe"]
        max_blocos = 10
        progresso = max(0, min(hp // 10, max_blocos))
        barra = "▰" * progresso + "▱" * (max_blocos - progresso)
        return f"**Status de {self.alvo.mention}:**\n❤️ HP: `{hp}`\n`[{barra}]`\n⚡ PE: `{pe}`"

    @discord.ui.button(label="-10", style=discord.ButtonStyle.danger, emoji="💥", row=0)
    async def tirar_10(self, interaction: discord.Interaction, button: discord.ui.Button):
        dados_rpg[self.alvo.id]["hp"] = max(0, dados_rpg[self.alvo.id]["hp"] - 10)
        salvar_dados(); await interaction.response.edit_message(content=self.gerar_barra())

    @discord.ui.button(label="-5", style=discord.ButtonStyle.danger, emoji="💥", row=0)
    async def tirar_5(self, interaction: discord.Interaction, button: discord.ui.Button):
        dados_rpg[self.alvo.id]["hp"] = max(0, dados_rpg[self.alvo.id]["hp"] - 5)
        salvar_dados(); await interaction.response.edit_message(content=self.gerar_barra())

    @discord.ui.button(label="+5", style=discord.ButtonStyle.success, emoji="❤️", row=0)
    async def dar_5(self, interaction: discord.Interaction, button: discord.ui.Button):
        dados_rpg[self.alvo.id]["hp"] += 5
        salvar_dados(); await interaction.response.edit_message(content=self.gerar_barra())

    @discord.ui.button(label="+10", style=discord.ButtonStyle.success, emoji="❤️", row=0)
    async def dar_10(self, interaction: discord.Interaction, button: discord.ui.Button):
        dados_rpg[self.alvo.id]["hp"] += 10
        salvar_dados(); await interaction.response.edit_message(content=self.gerar_barra())

    @discord.ui.button(label="-1", style=discord.ButtonStyle.secondary, emoji="💥", row=1)
    async def tirar_1(self, interaction: discord.Interaction, button: discord.ui.Button):
        dados_rpg[self.alvo.id]["hp"] = max(0, dados_rpg[self.alvo.id]["hp"] - 1)
        salvar_dados(); await interaction.response.edit_message(content=self.gerar_barra())

    @discord.ui.button(label="+1", style=discord.ButtonStyle.secondary, emoji="❤️", row=1)
    async def dar_1(self, interaction: discord.Interaction, button: discord.ui.Button):
        dados_rpg[self.alvo.id]["hp"] += 1
        salvar_dados(); await interaction.response.edit_message(content=self.gerar_barra())

# --- CLASSE PAINEL DE ESFORÇO (PE) ---
class PainelPE(discord.ui.View):
    def __init__(self, alvo):
        super().__init__(timeout=None)
        self.alvo = alvo

    def gerar_barra_pe(self):
        garantir_usuario(self.alvo.id)
        pe = dados_rpg[self.alvo.id]["pe"]
        hp = dados_rpg[self.alvo.id]["hp"]
        max_blocos = 10
        progresso = max(0, min(pe // 5, max_blocos)) 
        barra = "🔵" * progresso + "⚪" * (max_blocos - progresso)
        return f"**Energia de {self.alvo.mention}:**\n⚡ PE: `{pe}`\n`[{barra}]`\n❤️ HP Atual: `{hp}`"

    @discord.ui.button(label="-5", style=discord.ButtonStyle.danger, emoji="⚡", row=0)
    async def gastar_5(self, interaction: discord.Interaction, button: discord.ui.Button):
        dados_rpg[self.alvo.id]["pe"] = max(0, dados_rpg[self.alvo.id]["pe"] - 5)
        salvar_dados(); await interaction.response.edit_message(content=self.gerar_barra_pe())

    @discord.ui.button(label="-1", style=discord.ButtonStyle.secondary, emoji="⚡", row=0)
    async def gastar_1(self, interaction: discord.Interaction, button: discord.ui.Button):
        dados_rpg[self.alvo.id]["pe"] = max(0, dados_rpg[self.alvo.id]["pe"] - 1)
        salvar_dados(); await interaction.response.edit_message(content=self.gerar_barra_pe())

    @discord.ui.button(label="+1", style=discord.ButtonStyle.secondary, emoji="⚡", row=0)
    async def ganhar_1(self, interaction: discord.Interaction, button: discord.ui.Button):
        dados_rpg[self.alvo.id]["pe"] += 1
        salvar_dados(); await interaction.response.edit_message(content=self.gerar_barra_pe())

    @discord.ui.button(label="+5", style=discord.ButtonStyle.success, emoji="⚡", row=0)
    async def ganhar_5(self, interaction: discord.Interaction, button: discord.ui.Button):
        dados_rpg[self.alvo.id]["pe"] += 5
        salvar_dados(); await interaction.response.edit_message(content=self.gerar_barra_pe())

# --- CLASSE PAINEL DE SANIDADE (SAN) ---
class PainelSanidade(discord.ui.View):
    def __init__(self, alvo):
        super().__init__(timeout=None)
        self.alvo = alvo

    def gerar_barra_san(self):
        garantir_usuario(self.alvo.id)
        san = dados_rpg[self.alvo.id]["san"]
        max_blocos = 10
        progresso = max(0, min(san // 10, max_blocos))
        # Barra roxa para sanidade
        barra = "🟣" * progresso + "⚫" * (max_blocos - progresso)
        return f"**Mente de {self.alvo.mention}:**\n🧠 Sanidade: `{san}`\n`[{barra}]`"

    # Botões de Loucura (Dano Mental)
    @discord.ui.button(label="-10", style=discord.ButtonStyle.danger, emoji="👁️", row=0)
    async def perder_10(self, interaction: discord.Interaction, button: discord.ui.Button):
        dados_rpg[self.alvo.id]["san"] = max(0, dados_rpg[self.alvo.id]["san"] - 10)
        salvar_dados(); await interaction.response.edit_message(content=self.gerar_barra_san())

    @discord.ui.button(label="-5", style=discord.ButtonStyle.danger, emoji="👁️", row=0)
    async def perder_5(self, interaction: discord.Interaction, button: discord.ui.Button):
        dados_rpg[self.alvo.id]["san"] = max(0, dados_rpg[self.alvo.id]["san"] - 5)
        salvar_dados(); await interaction.response.edit_message(content=self.gerar_barra_san())

    # Botões de Recuperação (Terapia/Descanso)
    @discord.ui.button(label="+5", style=discord.ButtonStyle.primary, emoji="🧠", row=0)
    async def ganhar_5(self, interaction: discord.Interaction, button: discord.ui.Button):
        dados_rpg[self.alvo.id]["san"] += 5
        salvar_dados(); await interaction.response.edit_message(content=self.gerar_barra_san())

    @discord.ui.button(label="+10", style=discord.ButtonStyle.primary, emoji="🧠", row=0)
    async def ganhar_10(self, interaction: discord.Interaction, button: discord.ui.Button):
        dados_rpg[self.alvo.id]["san"] += 10
        salvar_dados(); await interaction.response.edit_message(content=self.gerar_barra_san())

# --- EVENTOS ---
@bot.event
async def on_ready():
    print(f"✅ Bot RPG Online: {bot.user.name}")

# --- PANIEL DE AJUDA---
@bot.command()
async def ajuda(ctx):
    embed = discord.Embed(title="📜 Comandos do RPG", color=0x00ff00)
    embed.add_field(name="Paineis", value="`.contvida @user`\n`.contpe @user`\n`.contsan @user` (Sanidade)", inline=False)
    embed.add_field(name="Configuração", value="`.setvida`, `.setpe`, `.setsan`", inline=False)
    await ctx.send(embed=embed)

# --- COMANDOS DE PAINEIS (Vida, PE, Sanidade) ---

@bot.command()
async def contvida(ctx, alvo: discord.Member):
    garantir_usuario(alvo.id)
    view = PainelVida(alvo)
    await ctx.send(view.gerar_barra(), view=view)

@bot.command()
async def contpe(ctx, alvo: discord.Member):
    garantir_usuario(alvo.id)
    view = PainelPE(alvo)
    await ctx.send(view.gerar_barra_pe(), view=view)

@bot.command()
async def contsan(ctx, alvo: discord.Member):
    garantir_usuario(alvo.id)
    view = PainelSanidade(alvo)
    await ctx.send(view.gerar_barra_san(), view=view)

# --- COMANDOS DE SETAR VALORES ---

@bot.command()
async def setvida(ctx, alvo: discord.Member, valor: int):
    garantir_usuario(alvo.id)
    dados_rpg[alvo.id]["hp"] = valor
    salvar_dados()
    await ctx.reply(f"✅ HP de **{alvo.display_name}** definido para **{valor}**.")

@bot.command()
async def setpe(ctx, alvo: discord.Member, valor: int):
    garantir_usuario(alvo.id)
    dados_rpg[alvo.id]["pe"] = valor
    salvar_dados()
    await ctx.reply(f"✅ PE de **{alvo.display_name}** definido para **{valor}**.")

@bot.command()
async def setsan(ctx, alvo: discord.Member, valor: int):
    garantir_usuario(alvo.id)
    dados_rpg[alvo.id]["san"] = valor
    salvar_dados()
    await ctx.reply(f"✅ Sanidade de **{alvo.display_name}** definida para **{valor}**.")

# --- COMANDOS EXCLUSIVOS DO MESTRE ---

@bot.command()
@commands.has_any_role("Mestre do Abismo")
async def dano(ctx, alvo: discord.Member, quantidade: int):
    garantir_usuario(alvo.id)
    dados_rpg[alvo.id]["hp"] = max(0, dados_rpg[alvo.id]["hp"] - quantidade)
    salvar_dados()
    await ctx.send(f"💥 **{alvo.display_name}** tomou **{quantidade}** de dano! HP: `{dados_rpg[alvo.id]['hp']}`")

@bot.command()
@commands.has_any_role("Mestre do Abismo")
async def curar(ctx, alvo: discord.Member, quantidade: int):
    garantir_usuario(alvo.id)
    dados_rpg[alvo.id]["hp"] += quantidade
    salvar_dados()
    await ctx.send(f"✨ **{alvo.display_name}** curou **{quantidade}**! HP: `{dados_rpg[alvo.id]['hp']}`")

@bot.command()
@commands.has_any_role("Mestre do Abismo")
async def tirarpe(ctx, alvo: discord.Member, quantidade: int):
    garantir_usuario(alvo.id)
    dados_rpg[alvo.id]["pe"] = max(0, dados_rpg[alvo.id]["pe"] - quantidade)
    salvar_dados()
    await ctx.send(f"📉 **{alvo.display_name}** perdeu **{quantidade}** de PE! Atual: `{dados_rpg[alvo.id]['pe']}`")

@bot.command()
@commands.has_any_role("Mestre do Abismo")
async def darpe(ctx, alvo: discord.Member, quantidade: int):
    garantir_usuario(alvo.id)
    dados_rpg[alvo.id]["pe"] += quantidade
    salvar_dados()
    await ctx.send(f"🌀 **{alvo.display_name}** recuperou **{quantidade}** de PE! Atual: `{dados_rpg[alvo.id]['pe']}`")

@bot.command()
@commands.has_any_role("Mestre do Abismo")
async def tirarsan(ctx, alvo: discord.Member, quantidade: int):
    garantir_usuario(alvo.id)
    dados_rpg[alvo.id]["san"] = max(0, dados_rpg[alvo.id]["san"] - quantidade)
    salvar_dados()
    await ctx.send(f"👁️ **{alvo.display_name}** perdeu **{quantidade}** de Sanidade! Atual: `{dados_rpg[alvo.id]['san']}`")

@bot.command()
@commands.has_any_role("Mestre do Abismo")
async def darsan(ctx, alvo: discord.Member, quantidade: int):
    garantir_usuario(alvo.id)
    dados_rpg[alvo.id]["san"] += quantidade
    salvar_dados()
    await ctx.send(f"🧠 **{alvo.display_name}** recuperou **{quantidade}** de Sanidade! Atual: `{dados_rpg[alvo.id]['san']}`")

@bot.command()
@commands.has_any_role("Mestre do Abismo")
async def limparplayer(ctx):
    # Avisa que vai começar (apaga a mensagem do comando do usuário primeiro)
    await ctx.message.delete()
    
    # Função de verificação: Retorna True se a mensagem deve ser apagada
    # Lógica: Se o autor da mensagem NÃO for o bot, apaga.
    def deve_apagar(m):
        return m.author != ctx.bot.user

    # O limit=None varre o canal todo. O check garante que o bot é salvo.
    await ctx.channel.purge(limit=None, check=deve_apagar)

    # Envia um aviso final que se autodestrói em 5 segundos para deixar o chat limpo
    msg = await ctx.send("🧹 **Limpeza concluída!** Mantive apenas os painéis e mensagens do sistema.")
    await msg.delete(delay=5)


# --- COMANDO: LIMPAR SÓ O BOT ---
@bot.command()
@commands.has_any_role("Mestre do Abismo")
async def limparbot(ctx):
    # Apaga o comando que você digitou primeiro
    await ctx.message.delete()

    # Função que verifica se a mensagem é do próprio bot
    def eh_o_bot(m):
        return m.author == ctx.bot.user

    # Apaga todas as mensagens onde 'eh_o_bot' for verdade
    removidas = await ctx.channel.purge(limit=None, check=eh_o_bot)
    
    # Aviso temporário
    msg = await ctx.send(f"🤖 Removi **{len(removidas)}** mensagens minhas/paineis.")
    await msg.delete(delay=5)

# --- COMANDO: LIMPAR TUDO (Reset Geral) ---
@bot.command()
@commands.has_any_role("Mestre do Abismo")
async def limpar(ctx):
    # O purge sem 'check' apaga tudo que vê pela frente
    await ctx.channel.purge(limit=None)
    
    # Aviso temporário
    msg = await ctx.send("💥 **O Abismo consumiu tudo!** (Chat limpo)")
    await msg.delete(delay=5)

@bot.event
async def on_message(message):
    # 1. Ignora mensagens do próprio bot
    if message.author == bot.user:
        return

    # 2. Verifica se a pessoa falou "bom dia"
    if "bom dia" in message.content.lower():
        # URL do GIF (Este é o do Thomas Shelby, pode trocar se quiser)
        gif_url = "https://i.pinimg.com/originals/ff/ad/b7/ffadb7e3f7ac71bd000bf4976f970fcd.gif"
        
        # Cria o Embed (o "cartão" invisível que segura a imagem)
        embed = discord.Embed(color=0x2f3136) # Cor escura para ficar discreto
        embed.set_image(url=gif_url)

        # Envia a mensagem de texto E o embed juntos
        await message.reply("Bom dia, Magnata! 🍷🗿", embed=embed)

    # 3. Mantém os outros comandos funcionando
    await bot.process_commands(message)

# Tratamento de Erro para quem não tem o cargo
@dano.error
@curar.error
@tirarpe.error
@darpe.error
@tirarsan.error
@darsan.error
async def mestre_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.reply("❌ Comando restrito ao **Mestre do Abismo**!")

bot.run("")