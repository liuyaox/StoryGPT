import streamlit as st

st.title("StoryGPT")

st.text("Please add all the information to create your world in the pages to the side, check what you have done it world_secription page to have AI help use llama_help page and open it a in a separate folder")

button_pressed= st.button("Generate Story")

from typing import List, Dict, Callable
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    BaseMessage,
)

class DialogueAgent:
    def __init__(
        self,
        name: str,
        system_message: SystemMessage,
        model: ChatOpenAI,
    ) -> None:
        self.name = name
        self.system_message = system_message
        self.model = model
        self.prefix = f"{self.name}: "
        self.reset()

    def reset(self):
        self.message_history = ["Here is the conversation so far."]

    def send(self) -> str:
        """
        Applies the chatmodel to the message history
        and returns the message string
        """
        message = self.model(
            [
                self.system_message,
                HumanMessage(content="\n".join(self.message_history + [self.prefix])),
            ]
        )
        return message.content

    def receive(self, name: str, message: str) -> None:
        """
        Concatenates {message} spoken by {name} into message history
        """
        self.message_history.append(f"{name}: {message}")


class DialogueSimulator:
    def __init__(
        self,
        agents: List[DialogueAgent],
        selection_function: Callable[[int, List[DialogueAgent]], int],
    ) -> None:
        self.agents = agents
        self._step = 0
        self.select_next_speaker = selection_function

    def reset(self):
        for agent in self.agents:
            agent.reset()

    def inject(self, name: str, message: str):
        """
        Initiates the conversation with a {message} from {name}
        """
        for agent in self.agents:
            agent.receive(name, message)

        # increment time
        self._step += 1

    def step(self) -> tuple[str, str]:
        # 1. choose the next speaker
        speaker_idx = self.select_next_speaker(self._step, self.agents)
        speaker = self.agents[speaker_idx]

        # 2. next speaker sends message
        message = speaker.send()

        # 3. everyone receives message
        for receiver in self.agents:
            receiver.receive(speaker.name, message)

        # 4. increment time
        self._step += 1

        return speaker.name, message
    
def select_next_speaker(step: int, agents: List[DialogueAgent]) -> int:

    if step % 2 == 0:
        idx = 0
    else:
        idx = (step // 2) % (len(agents) - 1) + 1
    return idx
    
from world_description import world, locations, mcguffins, characters

word_limit=50
storyteller_name='whimsy'
storyteller_system_message = SystemMessage(
    content=(
        f"""{world.name} is a Fntasy Adventure World. {world.Plot}. {world.History}. {world.mcguffins}
You are the storyteller, {storyteller_name}. 
The other players will propose actions to take and you will explain what happens when they take those actions.
Speak in the first person from the perspective of {storyteller_name}.
Do not change roles!
Do not speak from the perspective of anyone else.
Remember you are the storyteller, {storyteller_name}.
Stop speaking the moment you finish speaking from your perspective.
Never forget to keep your response to {word_limit} words!
Do not add anything else.
""")
)
storyteller = DialogueAgent(
    name=storyteller_name,
    system_message=storyteller_system_message,
    model=ChatOpenAI(temperature=0.2),
)
characters_name= [character.name for character in characters]
character_system_messages = [character.description for character in characters]
character = []
for character_name, character_system_message in zip(
    characters_name, character_system_messages
):
    characters.append(
        DialogueAgent(
            name=character_name,
            system_message=character_system_message,
            model=ChatOpenAI(temperature=0.2),
        )
    )

if button_pressed:
    max_iters = 20
    n = 0
    specified_quest="""Quest for the Shard of Eclipsed Memories:

    Artifact: The Shard of Eclipsed Memories is a fragment of the amulet that holds memories of the Primorials' final days. It is said to reside within the Caverns of Echoed Dreams.
    Quest: Elara and Kael must navigate the treacherous caverns, where they encounter illusions, riddles, and echoes of the past. They must confront their own memories and fears to reach the shard. Along the way, they encounter a ghostly guardian who guides them and tests their resolve."""
    simulator = DialogueSimulator(
        agents=[storyteller] + character, selection_function=select_next_speaker
    )
    simulator.reset()
    simulator.inject(storyteller_name, specified_quest)
    print(f"({storyteller_name}): {specified_quest}")
    print("\n")

    while n < max_iters:
        name, message = simulator.step()
        print(f"({name}): {message}")
        print("\n")
        n += 1