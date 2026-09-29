import discord
from database import add_point


class AnswerView(discord.ui.View):
    def __init__(self, answers, correct):
        super().__init__(timeout=30)   # seconds before the question expires
        self.correct = correct
        self.answered = set()          # user IDs who already guessed
        self.message = None

        for answer in answers:
            button = discord.ui.Button(
                label=answer, style=discord.ButtonStyle.primary)
            button.callback = self.make_callback(answer)
            self.add_item(button)

    def make_callback(self, answer):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id in self.answered:
                await interaction.response.send_message("You already answered!", ephemeral=True)
                return
            self.answered.add(interaction.user.id)

            if answer == self.correct:
                self.disable_all()
                self.stop()
                await add_point(interaction.guild_id, interaction.user.id)
                await interaction.response.edit_message(view=self)
                await interaction.followup.send(
                    f"🎉 {interaction.user.mention} got it! The answer was **{self.correct}**. (+1 point)"
                )
            else:
                await interaction.response.send_message("Wrong answer!", ephemeral=True)
        return callback

    def disable_all(self):
        for item in self.children:
            item.disabled = True

    async def on_timeout(self):
        self.disable_all()
        if self.message:
            await self.message.edit(view=self)
            await self.message.reply(f"⏰ Time's up! The answer was **{self.correct}**.")
