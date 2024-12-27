import random
class PirateEasterEggs:
    def __init__(self):
        self.parrot_mode = False
        self.secret_commands = {
            'arrrrr': self._handle_arrr,
            'x marks the spot': self._handle_treasure_map,
            'polly wants a cracker': self._toggle_parrot_mode,
        }
        self.pirate_poems = [
            """
Yo ho ho and a bottle of rum!
Through stormy seas we've just begun,
With code that flows like ocean's tide,
In Maroon's syntax we take pride!
            """,
            """
A pirate's life is wild and free,
Just like this code you're bout to see,
With functions sailed and variables true,
This language's made for coders like you!
            """
        ]
    
    def _handle_arrr(self):
        poem = random.choice(self.pirate_poems)
        print("\n🏴‍☠️ Yarr! You've unlocked a pirate poem! 🏴‍☠️")
        print(poem)
        return True

    def _handle_treasure_map(self):
        print("\n🗺️  You've found a secret treasure map! 🗺️")
        print("""
    .    _..._  .   
   .   .'     '.   .
  .   .`  ^ ^  `.   .
 .    |  (o)(o)  |    .
.     |   ___)    |     .
   .  |  '''''  |  .   
     |         |   
     |    |    |    
      '.__|__.'    
       |     |     
   ____|_____|____
        """)
        return True

    def _toggle_parrot_mode(self):
        self.parrot_mode = not self.parrot_mode
        if self.parrot_mode:
            print("\n🦜 Squawk! Parrot mode activated! All your outputs will be repeated! 🦜")
        else:
            print("\n🦜 Parrot mode deactivated!")
        return True

    def check_for_easter_eggs(self, command: str) -> bool:
        clean_command = command.strip().lower()
        for secret, handler in self.secret_commands.items():
            if secret in clean_command:
                return handler()
        return False
