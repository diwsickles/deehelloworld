#!/usr/bin/env python3
"""
The Rookie: Badge of Honor
An Ethical Puzzle Game based on the TV Show "The Rookie"

A standalone game for MacBook featuring moral dilemmas, evidence analysis,
and decision-making puzzles inspired by the LAPD rookie experience.
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
import json
import random
from dataclasses import dataclass
from typing import List, Dict, Optional, Callable
from enum import Enum
import os


class GameState(Enum):
    MAIN_MENU = "main_menu"
    SCENARIO_INTRO = "scenario_intro"
    PUZZLE = "puzzle"
    CHOICE = "choice"
    OUTCOME = "outcome"
    GAME_OVER = "game_over"
    CREDITS = "credits"


@dataclass
class Choice:
    text: str
    integrity_change: int
    outcome_text: str
    leads_to: Optional[str] = None


@dataclass
class Puzzle:
    puzzle_type: str  # "evidence", "sequence", "logic", "witness"
    question: str
    options: List[str]
    correct_answer: int
    hint: str
    explanation: str


@dataclass
class Scenario:
    id: str
    title: str
    intro_text: str
    situation_text: str
    puzzle: Optional[Puzzle]
    choices: List[Choice]
    background_context: str


class GameData:
    """Contains all game scenarios and puzzles"""

    @staticmethod
    def get_scenarios() -> List[Scenario]:
        return [
            Scenario(
                id="first_day",
                title="Episode 1: First Day on the Beat",
                intro_text="""Welcome to the Los Angeles Police Department, rookie.

You're Officer Alex Chen, fresh out of the academy. Today is your first day
on patrol with your Training Officer, Angela Martinez.

"Remember," T.O. Martinez says, adjusting her sunglasses, "out here, every
decision matters. The badge doesn't make you right - your choices do."

Your radio crackles to life...""",
                situation_text="""DISPATCH: "7-Adam-19, respond to a 415 - disturbance at
Maple Street Market. Caller reports shoplifting suspect detained by store owner."

You arrive to find an elderly man in his 70s being held by a young store clerk.
The old man's pockets contain a loaf of bread and some cheese. He's trembling.

Store Clerk: "Caught him red-handed! I want him arrested!"

The elderly man looks at you with tears in his eyes: "I... I haven't eaten in
three days. My social security check doesn't come until next week. Please..."

T.O. Martinez watches you carefully. "Your call, rookie." """,
                background_context="First test of balancing law enforcement with compassion",
                puzzle=Puzzle(
                    puzzle_type="evidence",
                    question="""Before making your decision, assess the situation.

Which observation is MOST relevant to determining the appropriate response?""",
                    options=[
                        "The total value of stolen items appears to be under $20",
                        "The store clerk seems very angry",
                        "The elderly man's clothes are worn but clean",
                        "There are security cameras in the store"
                    ],
                    correct_answer=0,
                    hint="Consider what factors affect whether this is a misdemeanor or felony, and what options that gives you.",
                    explanation="""Correct! In California, theft under $950 is petty theft (misdemeanor).
For minor first offenses, officers have discretion. The low value opens up
alternatives to arrest, like a civil compromise between parties."""
                ),
                choices=[
                    Choice(
                        text="Arrest the man - theft is theft, regardless of circumstances",
                        integrity_change=-5,
                        outcome_text="""You arrest the elderly man. He's processed, spends the night in jail,
and receives a court date. The charges are eventually dropped, but he loses
his subsidized housing due to the arrest record.

T.O. Martinez: "Technically correct. But was justice served? Sometimes the law
gives us discretion for a reason."

You followed the letter of the law, but something feels hollow."""
                    ),
                    Choice(
                        text="Mediate - offer to pay for the items yourself and let him go with a warning",
                        integrity_change=10,
                        outcome_text="""You pull out $15 and pay for the items. You also give the man a card
for the local food bank and senior services.

The store clerk nods, satisfied. The elderly man weeps with gratitude.

T.O. Martinez smiles slightly: "That came out of your own pocket, rookie.
But you just showed what community policing really means. Well done."

You upheld justice while showing compassion."""
                    ),
                    Choice(
                        text="Look the other way - pretend you didn't see anything",
                        integrity_change=-10,
                        outcome_text="""You tell the clerk you can't do anything without proof. The clerk is
furious and calls your supervisor to complain.

T.O. Martinez pulls you aside: "I saw everything, rookie. Ignoring a crime
isn't compassion - it's dereliction of duty. There were better options."

You tried to help but chose the wrong way."""
                    ),
                    Choice(
                        text="Facilitate a civil compromise - have the clerk agree not to press charges if restitution is made",
                        integrity_change=15,
                        outcome_text="""You calmly explain California's civil compromise law to both parties.
The clerk agrees to drop it if the man returns the items and promises not
to return. You connect the man with social services.

T.O. Martinez nods approvingly: "Textbook community policing. You used your
knowledge of the law to find a solution that works for everyone. The best
officers know when NOT to make an arrest."

You demonstrated wisdom beyond your experience."""
                    )
                ]
            ),

            Scenario(
                id="domestic_call",
                title="Episode 2: Behind Closed Doors",
                intro_text="""Two weeks into your training. You've handled traffic stops,
minor disturbances, and even a car chase. But tonight brings something different.

T.O. Martinez's expression is serious as she briefs you in the car.

"Domestic calls are the most dangerous. Emotions run high. People are
unpredictable. Stay sharp, watch the hands, and remember - our job is
everyone's safety, including our own."

The call comes through...""",
                situation_text="""DISPATCH: "7-Adam-19, domestic disturbance at 4521 Oak Avenue,
Apartment 3B. Neighbors report shouting, sounds of breaking glass."

You arrive at a modest apartment. A woman in her 30s opens the door. She has
a fresh bruise forming under her eye but smiles nervously.

Woman: "Officers, there's been a mistake. We were just... watching a movie.
Everything is fine here."

Behind her, you see broken glass on the floor. A man sits on the couch,
watching you with cold eyes. The woman's hands are shaking.

T.O. Martinez speaks softly: "Ma'am, we need to come in and make sure
everyone's okay. It's standard procedure." """,
                background_context="Recognizing signs of domestic abuse and navigating victim reluctance",
                puzzle=Puzzle(
                    puzzle_type="witness",
                    question="""As you enter, you need to assess safety and gather information.

What should be your FIRST priority?""",
                    options=[
                        "Immediately arrest the man based on the visible bruise",
                        "Separate the parties to speak with them individually",
                        "Ask the woman directly if she's being abused",
                        "Search the apartment for weapons"
                    ],
                    correct_answer=1,
                    hint="Victims often can't speak freely in the presence of their abuser.",
                    explanation="""Correct! Separating parties is crucial in domestic calls. Victims
often minimize abuse when the abuser is present due to fear. Speaking
privately allows honest communication and proper assessment."""
                ),
                choices=[
                    Choice(
                        text="Respect her wishes - she says everything is fine, so leave",
                        integrity_change=-15,
                        outcome_text="""You accept her statement and leave. Three days later, you respond
to the same address. This time, she's in the hospital with broken ribs
and a fractured jaw.

T.O. Martinez finds you in the locker room: "I know this is hard. But when
someone's safety is at risk, we have a duty to dig deeper. She wasn't able
to tell us the truth with him right there."

The weight of what might have been prevented haunts you."""
                    ),
                    Choice(
                        text="Arrest the man immediately - the bruise is evidence enough",
                        integrity_change=-5,
                        outcome_text="""You arrest the man. However, without proper documentation and the
victim's cooperation, the DA declines to prosecute. The man returns home
angrier than before. The woman blames you for making things worse.

T.O. Martinez: "Your heart was in the right place, but we needed to build
a proper case. Quick action isn't always the right action."

Good intentions led to a worse outcome."""
                    ),
                    Choice(
                        text="Ask T.O. Martinez to talk to the woman privately while you speak with the man",
                        integrity_change=15,
                        outcome_text="""With the parties separated, T.O. Martinez learns the woman has been
enduring abuse for months. She was afraid to speak with him present.

Meanwhile, the man becomes aggressive with you, confirming the danger.
You document everything properly. The woman agrees to press charges and
is connected with a domestic violence shelter.

T.O. Martinez: "That's how it's done, rookie. You gave her a safe space
to tell her truth. Today, you may have saved a life."

Professional procedure led to a breakthrough."""
                    ),
                    Choice(
                        text="Document the visible injuries and offer her resources, even if she won't press charges",
                        integrity_change=10,
                        outcome_text="""You can't force her to cooperate, but you thoroughly document the
bruise with photos, give her domestic violence hotline information, and
file a detailed report.

Two weeks later, she calls that hotline and eventually leaves him safely.

T.O. Martinez: "Sometimes we plant seeds. You gave her tools and let her
know someone cared. That matters more than you know."

Patience and compassion paid off."""
                    )
                ]
            ),

            Scenario(
                id="partner_dilemma",
                title="Episode 3: The Blue Wall",
                intro_text="""A month on the job. You've started to feel like a real cop.
You know the regulars, the shortcuts, the rhythm of the streets.

But today, T.O. Martinez is off, and you're paired with Officer Derek
Simmons - a 15-year veteran with a reputation for "getting results."

As you patrol, you notice he's... different. More aggressive. More shortcuts.

"Relax, rookie," Simmons says, noticing your expression. "The academy
teaches you the rules. I'm gonna teach you how the real world works."

Then you see something you can't ignore...""",
                situation_text="""During a routine traffic stop, Officer Simmons pulls over a young
Black man for a broken taillight. The driver is nervous but cooperative,
providing license and registration immediately.

While you run his information (which comes back clean), you watch Simmons
order the man out of the car and conduct an aggressive search. The driver
protests but complies.

Simmons finds nothing illegal. But then he reaches into his own pocket,
pulls out a small bag of marijuana, and says loudly:

"Well, well, what do we have here?"

He looks at you with a cold smile. "You saw him drop this, right rookie?"

The driver's eyes go wide with terror. "That's not mine! Officer, please!"

Simmons is waiting for your answer.""",
                background_context="Testing integrity when faced with corruption from fellow officers",
                puzzle=Puzzle(
                    puzzle_type="logic",
                    question="""You're being asked to be complicit in planting evidence.

What factors should MOST influence your decision?""",
                    options=[
                        "Your career could be destroyed if you contradict a veteran",
                        "The driver might actually be guilty of something else",
                        "You have a sworn duty to uphold the law, even against fellow officers",
                        "No one else saw what happened, so it's your word against his"
                    ],
                    correct_answer=2,
                    hint="What did you swear to do when you took the oath?",
                    explanation="""Correct. Your oath is to protect and serve the public and uphold
the Constitution. That duty doesn't have exceptions for fellow officers.
Integrity is the foundation of legitimate law enforcement."""
                ),
                choices=[
                    Choice(
                        text="Go along with it - Simmons is a veteran, and you need to pick your battles",
                        integrity_change=-30,
                        outcome_text="""You nod silently. The innocent man is arrested. He loses his job,
his apartment, and three months of his life fighting the charges.

The case eventually falls apart when Simmons tries this again and gets
caught. The investigation reveals your complicity. You're fired and
charged as an accessory.

As they take your badge, you remember the driver's eyes. The moment you
chose silence over justice, you stopped being a cop.

Career and honor: both lost."""
                    ),
                    Choice(
                        text="Refuse to corroborate - tell Simmons you can't lie",
                        integrity_change=10,
                        outcome_text="""You shake your head. "I didn't see him drop anything, Officer Simmons."

Simmons glares at you but can't proceed without a witness. He pockets the
bag and tells the driver to "get out of here."

The ride back is silent and hostile. Simmons makes your life difficult for
weeks. But you can look at yourself in the mirror.

T.O. Martinez hears about it: "That took guts, rookie. Real guts."

You kept your integrity but made an enemy."""
                    ),
                    Choice(
                        text="Immediately report what you witnessed to your supervisor",
                        integrity_change=25,
                        outcome_text="""You excuse yourself to make a "routine call" and immediately contact
Sergeant Grey. Within the hour, Internal Affairs is involved.

Simmons is suspended, then fired. Investigation reveals a pattern of
misconduct going back years. Several wrongful convictions are overturned.

The driver thanks you personally. "You gave me my faith back," he says.

It's hard. Some officers shun you. But the ones who matter respect you more.

T.O. Martinez: "You just proved you're the real deal. Welcome to the
right side of the thin blue line."

Justice served, at personal cost."""
                    ),
                    Choice(
                        text="De-escalate - suggest to Simmons that this isn't worth the paperwork",
                        integrity_change=0,
                        outcome_text="""You try diplomacy. "Hey, for a broken taillight? Lot of paperwork,
man. Let's just cut him loose."

Simmons hesitates, then pockets the bag. "Fine. Your loss, rookie."

The driver goes free, but you didn't address the real problem. Next week,
Simmons does the same thing to someone else, and this time succeeds.

You avoided immediate conflict but left a corrupt cop on the streets.

T.O. Martinez, later: "I heard what happened. I'm glad the guy went free,
but Simmons is still out there. Sometimes doing the right thing means
doing the hard thing."

A temporary fix, not a solution."""
                    )
                ]
            ),

            Scenario(
                id="hostage_crisis",
                title="Episode 4: The Breaking Point",
                intro_text="""Three months in. You've seen things. Good and bad. You've started
to understand that being a cop isn't about being a hero - it's about
being human in impossible situations.

Today starts normally. Then the call comes in.

"All units, Code 37, armed suspect with hostages at First National Bank,
Main Street. SWAT en route, ETA fifteen minutes."

You're two blocks away. T.O. Martinez accelerates.

"We're not going in," she says firmly. "Hostage situations are for SWAT.
We establish a perimeter and wait."

But as you arrive, you see something that changes everything...""",
                situation_text="""The bank's glass front is shattered. Inside, you can see a man with a
gun pressed to a woman's head. He's screaming, wild-eyed, desperate.

Then you recognize the hostage. It's Sarah Chen - your sister.

The gunman sees your uniform and screams: "STAY BACK OR SHE DIES!"

Sarah's eyes meet yours. She's terrified but trying to be brave. Just like
when you were kids.

T.O. Martinez grabs your arm. "Chen. CHEN. I see who that is. But you
cannot go in there. You're too close to this. You need to step back and
let the professionals handle it."

The gunman is getting more agitated. SWAT is still twelve minutes out.

Your sister mouths three words: "I love you."

What do you do?""",
                background_context="Testing judgment when personal stakes conflict with professional duty",
                puzzle=Puzzle(
                    puzzle_type="sequence",
                    question="""In hostage situations, what is the correct sequence of priorities?""",
                    options=[
                        "Neutralize threat, rescue hostages, preserve evidence",
                        "Safety of hostages, safety of bystanders, safety of officers, apprehend suspect",
                        "Wait for SWAT, establish perimeter, negotiate if possible",
                        "Identify suspect, assess weapons, count hostages, report to command"
                    ],
                    correct_answer=1,
                    hint="What is the fundamental priority order in any crisis situation?",
                    explanation="""Correct. The priority is always: hostage safety first, then public
safety, then officer safety, then apprehension. This guides all tactical
decisions. Personal connections don't change this calculus."""
                ),
                choices=[
                    Choice(
                        text="Rush in to save your sister - you can't just stand here",
                        integrity_change=-20,
                        outcome_text="""You break away from Martinez and charge in. The gunman panics and
fires. The bullet hits your vest, knocking you down.

In the chaos, SWAT arrives and breaches. The gunman is killed. Sarah is
physically unharmed but traumatized.

You're suspended for reckless endangerment. Your action could have gotten
multiple people killed, including Sarah.

Sarah, later: "I know you were trying to save me. But when you ran in, I
thought we were both going to die. Please... trust your training."

Love drove your action. Training should have."""
                    ),
                    Choice(
                        text="Stay back as ordered, but try to establish communication with the gunman",
                        integrity_change=15,
                        outcome_text="""Fighting every instinct, you follow protocol. You get on the PA system.

"Sir, my name is Officer Chen. I can see you're in pain. Talk to me. What
do you need?"

The gunman hesitates. He's not a hardened criminal - he's a man whose wife
just died, whose house is being foreclosed, who saw no other way.

Your calm voice keeps him talking until SWAT arrives. Negotiators take over.
An hour later, he surrenders. Sarah runs into your arms.

T.O. Martinez: "That was the hardest thing you'll ever do. And you did it
right. You saved her by trusting the process."

Professional discipline saved multiple lives."""
                    ),
                    Choice(
                        text="Request to be removed from the scene - you're too compromised",
                        integrity_change=10,
                        outcome_text="""You tell Martinez you can't be objective. She nods and has another
unit take your position while she stays on the perimeter.

You wait in the car, listening to the radio, every second agony.

SWAT resolves the situation. Sarah is safe. The gunman is in custody.

Sergeant Grey finds you afterward: "That took real self-awareness, Chen.
Knowing your limits is as important as knowing your strengths."

Sarah holds you as you finally let yourself cry.

You recognized your limitation and acted responsibly."""
                    ),
                    Choice(
                        text="Secretly position yourself for a shot - if things go bad, you'll end it",
                        integrity_change=-25,
                        outcome_text="""You slip away and find a vantage point. You draw your weapon.

T.O. Martinez finds you. She doesn't yell. She just says: "If you fire
that weapon, you'll start a massacre. Even if you hit him, his finger will
pull the trigger. Put it down, Chen. Now."

You lower the weapon, shaking. She's right. You almost made everything worse.

The situation ends peacefully when SWAT arrives. But Martinez writes you up.

"You're a good cop with good instincts," she says. "But today, emotion
almost made you a killer. Learn from this."

A close call with catastrophe."""
                    )
                ]
            ),

            Scenario(
                id="final_test",
                title="Episode 5: The Measure of a Badge",
                intro_text="""Six months. Your probationary period is ending. Tomorrow, you'll
be evaluated for permanent status.

T.O. Martinez has been quiet all day. Finally, she speaks.

"Chen, I've trained a lot of rookies. Some became good cops. Some washed
out. A few became great." She pauses. "You have the potential for great.
But this job tests you every single day. The question isn't whether you
CAN do the right thing. It's whether you WILL, when it costs you."

"Tonight is your last shift with me. Whatever happens, I want you to
remember: the badge is just metal. YOU decide what it means."

And then, as if the universe was listening, the call comes...""",
                situation_text="""It's a warehouse district. You're responding to shots fired.

You find chaos. Two gang members are down, wounded. A third is standing over
them with a gun - but he's not a gang member. He's Marcus Webb, a community
activist you've met before. He runs an after-school program for at-risk youth.

Marcus sees you and drops the gun. "Officer Chen! Thank God. These men - they
were about to execute a kid. A fourteen-year-old boy. I had to stop them."

You find the boy, Jaylen, hiding behind some crates. Terrified but unharmed.

Marcus: "They were going to kill him for trying to leave the gang. I heard it
happening and I... I grabbed one of their guns and..."

The gang members are alive but cursing, swearing revenge. Marcus looks at you.

"I know what I did was illegal. But that boy would be dead if I hadn't acted.
What are you going to charge me with? I'll accept the consequences."

T.O. Martinez watches. This is your call. Your final test.""",
                background_context="The ultimate test - balancing justice, law, and moral complexity",
                puzzle=Puzzle(
                    puzzle_type="logic",
                    question="""Analyze the legal and ethical dimensions of this situation.

Which statement BEST captures the complexity here?""",
                    options=[
                        "Marcus committed assault with a deadly weapon - the law is clear",
                        "Marcus acted in defense of another - a potential legal justification",
                        "The gang members are the real criminals - Marcus should be praised",
                        "This is above your pay grade - let the detectives figure it out"
                    ],
                    correct_answer=1,
                    hint="What legal doctrine might apply when someone uses force to protect another person?",
                    explanation="""Correct. 'Defense of others' is a legal justification that can apply
when someone uses reasonable force to protect a third party from imminent
harm. Marcus's actions may fall under this doctrine - but the determination
involves many factors that go beyond a patrol officer's arrest decision."""
                ),
                choices=[
                    Choice(
                        text="Arrest Marcus for assault - he admitted to shooting two people",
                        integrity_change=-5,
                        outcome_text="""You arrest Marcus. He goes quietly, still maintaining he'd do it again.

The gang members are arrested too. But in the legal process, Marcus's
defender-of-others argument is strong. The DA offers a plea deal that he
refuses. At trial, he's acquitted.

But those months in legal limbo damaged his program. Some kids fell through
the cracks. Jaylen's family had to relocate in fear.

T.O. Martinez: "The law is important. But so is judgment. Sometimes the
technically correct answer isn't the wisest one."

Justice served, but at unnecessary cost."""
                    ),
                    Choice(
                        text="Let Marcus go - he's a hero who saved a child's life",
                        integrity_change=-10,
                        outcome_text="""You tell Marcus to leave before backup arrives. He hesitates, but goes.

But there are witnesses. Other units saw Marcus at the scene. When the
investigation reveals you let him go, you're accused of favoritism and
obstruction. Your career is in jeopardy.

Marcus comes forward and confesses everything to save you. Now you're both
in trouble.

T.O. Martinez: "Your heart was in the right place. But you can't make
evidence disappear because you like someone's character. There's a process
for a reason."

Good intentions, bad execution."""
                    ),
                    Choice(
                        text="Detain everyone, document the scene meticulously, and let the system work",
                        integrity_change=20,
                        outcome_text="""You secure the scene properly. Marcus, the gang members, and Jaylen
are all interviewed. You write a detailed report that includes all of
Marcus's statements about why he acted.

The gang members are charged with conspiracy to commit murder. Based on
your thorough documentation, the DA reviews Marcus's case through the lens
of defense-of-others and declines to prosecute.

Marcus's program continues. Jaylen gets a fresh start. Justice is served.

T.O. Martinez smiles - a rare sight. "You did everything right, Chen. You
let the system work while making sure it had everything it needed.
That's real police work."

Perfect balance of duty and judgment."""
                    ),
                    Choice(
                        text="Testify on Marcus's behalf - advocate for him within the system",
                        integrity_change=10,
                        outcome_text="""You detain Marcus but immediately tell the responding detectives about
the full context. You advocate strongly for considering the circumstances.

Your passionate defense raises eyebrows - officers are supposed to be
objective. But your documentation is solid, and the story holds up.

Marcus's case is resolved favorably. But some colleagues question whether
you were too emotionally involved.

T.O. Martinez: "Your advocacy helped Marcus. But be careful about becoming
an activist in uniform. Document thoroughly, testify honestly, and let
the system make the call. That's where your power ends - and should end."

Good outcome, but boundaries were tested."""
                    )
                ]
            )
        ]


class RookiePuzzleGame:
    """Main game class for The Rookie: Badge of Honor"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("The Rookie: Badge of Honor")
        self.root.geometry("900x700")
        self.root.configure(bg='#1a1a2e')
        self.root.resizable(True, True)

        # Game state
        self.current_state = GameState.MAIN_MENU
        self.current_scenario_index = 0
        self.scenarios = GameData.get_scenarios()
        self.integrity_score = 50  # Start at 50/100
        self.choices_made = []
        self.puzzle_solved = False

        # Fonts
        self.title_font = font.Font(family="Helvetica", size=28, weight="bold")
        self.subtitle_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.body_font = font.Font(family="Helvetica", size=12)
        self.button_font = font.Font(family="Helvetica", size=11, weight="bold")

        # Colors
        self.colors = {
            'bg_dark': '#1a1a2e',
            'bg_medium': '#16213e',
            'bg_light': '#0f3460',
            'accent': '#e94560',
            'text_primary': '#ffffff',
            'text_secondary': '#a0a0a0',
            'success': '#4ecca3',
            'warning': '#ffc107',
            'danger': '#e94560'
        }

        # Main container
        self.main_frame = tk.Frame(root, bg=self.colors['bg_dark'])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Show main menu
        self.show_main_menu()

    def clear_frame(self):
        """Clear all widgets from main frame"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        """Display the main menu"""
        self.clear_frame()
        self.current_state = GameState.MAIN_MENU

        # Title
        title_frame = tk.Frame(self.main_frame, bg=self.colors['bg_dark'])
        title_frame.pack(pady=40)

        tk.Label(
            title_frame,
            text="THE ROOKIE",
            font=self.title_font,
            fg=self.colors['accent'],
            bg=self.colors['bg_dark']
        ).pack()

        tk.Label(
            title_frame,
            text="Badge of Honor",
            font=self.subtitle_font,
            fg=self.colors['text_primary'],
            bg=self.colors['bg_dark']
        ).pack(pady=(5, 0))

        tk.Label(
            title_frame,
            text="An Ethical Puzzle Game",
            font=self.body_font,
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_dark']
        ).pack(pady=(10, 0))

        # Description
        desc_frame = tk.Frame(self.main_frame, bg=self.colors['bg_medium'], padx=20, pady=20)
        desc_frame.pack(pady=30, fill=tk.X)

        description = """Step into the boots of a rookie LAPD officer facing real moral dilemmas.

Every choice shapes your character. Every puzzle tests your judgment.
The badge is just metal - YOU decide what it means.

Based on the hit TV series, experience the challenges of law enforcement
where the right answer isn't always clear, and integrity is your greatest weapon."""

        tk.Label(
            desc_frame,
            text=description,
            font=self.body_font,
            fg=self.colors['text_primary'],
            bg=self.colors['bg_medium'],
            justify=tk.CENTER,
            wraplength=700
        ).pack()

        # Buttons
        button_frame = tk.Frame(self.main_frame, bg=self.colors['bg_dark'])
        button_frame.pack(pady=30)

        self.create_button(
            button_frame,
            "New Game",
            self.start_new_game,
            self.colors['success']
        ).pack(pady=10)

        self.create_button(
            button_frame,
            "How to Play",
            self.show_instructions,
            self.colors['bg_light']
        ).pack(pady=10)

        self.create_button(
            button_frame,
            "Credits",
            self.show_credits,
            self.colors['bg_light']
        ).pack(pady=10)

        self.create_button(
            button_frame,
            "Quit",
            self.root.quit,
            self.colors['danger']
        ).pack(pady=10)

    def create_button(self, parent, text, command, color, width=25):
        """Create a styled button"""
        btn = tk.Button(
            parent,
            text=text,
            font=self.button_font,
            fg=self.colors['text_primary'],
            bg=color,
            activebackground=color,
            activeforeground=self.colors['text_primary'],
            width=width,
            height=2,
            relief=tk.FLAT,
            cursor="hand2",
            command=command
        )
        btn.bind('<Enter>', lambda e: btn.configure(bg=self.lighten_color(color)))
        btn.bind('<Leave>', lambda e: btn.configure(bg=color))
        return btn

    def lighten_color(self, hex_color):
        """Lighten a hex color"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        lighter = tuple(min(255, int(c * 1.2)) for c in rgb)
        return '#{:02x}{:02x}{:02x}'.format(*lighter)

    def show_instructions(self):
        """Show game instructions"""
        self.clear_frame()

        tk.Label(
            self.main_frame,
            text="How to Play",
            font=self.subtitle_font,
            fg=self.colors['accent'],
            bg=self.colors['bg_dark']
        ).pack(pady=20)

        instructions = """THE ROOKIE: BADGE OF HONOR

GAMEPLAY:
You will face 5 scenarios inspired by the TV show "The Rookie."
Each scenario presents a moral dilemma that real police officers might face.

PUZZLES:
Before making your choice, you'll solve a puzzle related to the situation.
These test your understanding of law enforcement procedures, evidence analysis,
and ethical reasoning. Solving puzzles correctly will help inform your decision.

CHOICES:
After the puzzle, you'll choose how to handle the situation.
Each choice affects your INTEGRITY SCORE (0-100).
Your choices reveal what kind of officer you'll become.

INTEGRITY SCORING:
- Start with 50 points
- Ethical choices increase your score
- Compromising choices decrease your score
- Your final score determines your ending

ENDINGS:
- 80-100: Exemplary Officer - You represent the best of law enforcement
- 60-79: Good Officer - You make mistakes but learn from them
- 40-59: Struggling Officer - The job's moral complexities challenge you
- 0-39: Compromised Officer - You've lost sight of why you wear the badge

Remember: There are no perfect answers. Only your judgment and your conscience."""

        text_frame = tk.Frame(self.main_frame, bg=self.colors['bg_medium'], padx=20, pady=20)
        text_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        tk.Label(
            text_frame,
            text=instructions,
            font=self.body_font,
            fg=self.colors['text_primary'],
            bg=self.colors['bg_medium'],
            justify=tk.LEFT,
            wraplength=700
        ).pack()

        self.create_button(
            self.main_frame,
            "Back to Menu",
            self.show_main_menu,
            self.colors['bg_light']
        ).pack(pady=20)

    def show_credits(self):
        """Show game credits"""
        self.clear_frame()
        self.current_state = GameState.CREDITS

        tk.Label(
            self.main_frame,
            text="Credits",
            font=self.subtitle_font,
            fg=self.colors['accent'],
            bg=self.colors['bg_dark']
        ).pack(pady=20)

        credits_text = """THE ROOKIE: BADGE OF HONOR
An Ethical Puzzle Game

Inspired by the ABC Television Series "The Rookie"
Created by Alexi Hawley

This game is a fan-made tribute exploring the ethical themes
and moral complexities portrayed in the show.

"The Rookie" follows John Nolan, the oldest rookie in the LAPD,
as he navigates the challenges of law enforcement while
maintaining his integrity and humanity.

Game Design & Development:
Created with Python and Tkinter

Special Thanks:
To the cast and crew of "The Rookie" for creating
a show that explores the human side of policing.

To Nathan Fillion, whose portrayal of John Nolan
reminds us that it's never too late to pursue your calling.

DISCLAIMER:
This is an unofficial fan game created for educational
and entertainment purposes. It is not affiliated with or
endorsed by ABC, eOne, or any entities associated with
"The Rookie" television series.

The scenarios presented are fictional and designed to
explore ethical decision-making. They do not represent
official LAPD procedures or policies.

"It's not about the badge. It's about what you do with it."
"""

        text_frame = tk.Frame(self.main_frame, bg=self.colors['bg_medium'], padx=20, pady=20)
        text_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        tk.Label(
            text_frame,
            text=credits_text,
            font=self.body_font,
            fg=self.colors['text_primary'],
            bg=self.colors['bg_medium'],
            justify=tk.CENTER,
            wraplength=700
        ).pack()

        self.create_button(
            self.main_frame,
            "Back to Menu",
            self.show_main_menu,
            self.colors['bg_light']
        ).pack(pady=20)

    def start_new_game(self):
        """Start a new game"""
        self.current_scenario_index = 0
        self.integrity_score = 50
        self.choices_made = []
        self.show_scenario_intro()

    def show_scenario_intro(self):
        """Show the introduction to current scenario"""
        self.clear_frame()
        self.current_state = GameState.SCENARIO_INTRO
        self.puzzle_solved = False

        scenario = self.scenarios[self.current_scenario_index]

        # Header
        header_frame = tk.Frame(self.main_frame, bg=self.colors['bg_dark'])
        header_frame.pack(fill=tk.X)

        tk.Label(
            header_frame,
            text=f"Scenario {self.current_scenario_index + 1} of {len(self.scenarios)}",
            font=self.body_font,
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_dark']
        ).pack(side=tk.LEFT)

        tk.Label(
            header_frame,
            text=f"Integrity: {self.integrity_score}/100",
            font=self.body_font,
            fg=self.get_integrity_color(),
            bg=self.colors['bg_dark']
        ).pack(side=tk.RIGHT)

        # Title
        tk.Label(
            self.main_frame,
            text=scenario.title,
            font=self.subtitle_font,
            fg=self.colors['accent'],
            bg=self.colors['bg_dark']
        ).pack(pady=20)

        # Intro text
        text_frame = tk.Frame(self.main_frame, bg=self.colors['bg_medium'], padx=20, pady=20)
        text_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Scrollable text
        canvas = tk.Canvas(text_frame, bg=self.colors['bg_medium'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_medium'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        tk.Label(
            scrollable_frame,
            text=scenario.intro_text,
            font=self.body_font,
            fg=self.colors['text_primary'],
            bg=self.colors['bg_medium'],
            justify=tk.LEFT,
            wraplength=700
        ).pack(pady=10, padx=10)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Continue button
        self.create_button(
            self.main_frame,
            "Continue to Situation",
            self.show_situation,
            self.colors['success']
        ).pack(pady=20)

    def show_situation(self):
        """Show the situation and puzzle"""
        self.clear_frame()
        self.current_state = GameState.PUZZLE

        scenario = self.scenarios[self.current_scenario_index]

        # Header
        header_frame = tk.Frame(self.main_frame, bg=self.colors['bg_dark'])
        header_frame.pack(fill=tk.X)

        tk.Label(
            header_frame,
            text=scenario.title,
            font=self.body_font,
            fg=self.colors['accent'],
            bg=self.colors['bg_dark']
        ).pack(side=tk.LEFT)

        tk.Label(
            header_frame,
            text=f"Integrity: {self.integrity_score}/100",
            font=self.body_font,
            fg=self.get_integrity_color(),
            bg=self.colors['bg_dark']
        ).pack(side=tk.RIGHT)

        # Situation text
        situation_frame = tk.Frame(self.main_frame, bg=self.colors['bg_medium'], padx=15, pady=15)
        situation_frame.pack(pady=10, fill=tk.X)

        tk.Label(
            situation_frame,
            text="THE SITUATION:",
            font=self.button_font,
            fg=self.colors['warning'],
            bg=self.colors['bg_medium']
        ).pack(anchor='w')

        tk.Label(
            situation_frame,
            text=scenario.situation_text,
            font=self.body_font,
            fg=self.colors['text_primary'],
            bg=self.colors['bg_medium'],
            justify=tk.LEFT,
            wraplength=700
        ).pack(pady=10)

        # Puzzle section
        if scenario.puzzle:
            puzzle_frame = tk.Frame(self.main_frame, bg=self.colors['bg_light'], padx=15, pady=15)
            puzzle_frame.pack(pady=10, fill=tk.X)

            tk.Label(
                puzzle_frame,
                text="ASSESSMENT PUZZLE:",
                font=self.button_font,
                fg=self.colors['success'],
                bg=self.colors['bg_light']
            ).pack(anchor='w')

            tk.Label(
                puzzle_frame,
                text=scenario.puzzle.question,
                font=self.body_font,
                fg=self.colors['text_primary'],
                bg=self.colors['bg_light'],
                justify=tk.LEFT,
                wraplength=700
            ).pack(pady=10)

            # Answer options
            self.puzzle_var = tk.IntVar(value=-1)

            for i, option in enumerate(scenario.puzzle.options):
                rb = tk.Radiobutton(
                    puzzle_frame,
                    text=option,
                    variable=self.puzzle_var,
                    value=i,
                    font=self.body_font,
                    fg=self.colors['text_primary'],
                    bg=self.colors['bg_light'],
                    selectcolor=self.colors['bg_medium'],
                    activebackground=self.colors['bg_light'],
                    activeforeground=self.colors['text_primary'],
                    cursor="hand2"
                )
                rb.pack(anchor='w', pady=5)

            # Hint button
            hint_btn = tk.Button(
                puzzle_frame,
                text="Show Hint",
                font=self.body_font,
                fg=self.colors['text_secondary'],
                bg=self.colors['bg_medium'],
                relief=tk.FLAT,
                cursor="hand2",
                command=lambda: self.show_hint(scenario.puzzle.hint)
            )
            hint_btn.pack(pady=10)

            # Submit puzzle button
            self.create_button(
                puzzle_frame,
                "Submit Answer",
                lambda: self.check_puzzle_answer(scenario.puzzle),
                self.colors['accent'],
                width=15
            ).pack(pady=10)

    def show_hint(self, hint):
        """Show puzzle hint"""
        messagebox.showinfo("Hint", hint)

    def check_puzzle_answer(self, puzzle):
        """Check if puzzle answer is correct"""
        selected = self.puzzle_var.get()

        if selected == -1:
            messagebox.showwarning("No Selection", "Please select an answer before submitting.")
            return

        if selected == puzzle.correct_answer:
            self.puzzle_solved = True
            messagebox.showinfo(
                "Correct!",
                f"Well analyzed!\n\n{puzzle.explanation}"
            )
        else:
            messagebox.showinfo(
                "Not Quite",
                f"That's not the best answer.\n\n{puzzle.explanation}"
            )

        self.show_choices()

    def show_choices(self):
        """Show the choices for current scenario"""
        self.clear_frame()
        self.current_state = GameState.CHOICE

        scenario = self.scenarios[self.current_scenario_index]

        # Header
        header_frame = tk.Frame(self.main_frame, bg=self.colors['bg_dark'])
        header_frame.pack(fill=tk.X)

        tk.Label(
            header_frame,
            text=scenario.title,
            font=self.body_font,
            fg=self.colors['accent'],
            bg=self.colors['bg_dark']
        ).pack(side=tk.LEFT)

        tk.Label(
            header_frame,
            text=f"Integrity: {self.integrity_score}/100",
            font=self.body_font,
            fg=self.get_integrity_color(),
            bg=self.colors['bg_dark']
        ).pack(side=tk.RIGHT)

        # Decision prompt
        tk.Label(
            self.main_frame,
            text="MAKE YOUR DECISION:",
            font=self.subtitle_font,
            fg=self.colors['warning'],
            bg=self.colors['bg_dark']
        ).pack(pady=20)

        # Brief situation reminder
        tk.Label(
            self.main_frame,
            text=f"You've assessed the situation. Now, what do you do?",
            font=self.body_font,
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_dark']
        ).pack(pady=10)

        # Choice buttons
        choices_frame = tk.Frame(self.main_frame, bg=self.colors['bg_dark'])
        choices_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        for i, choice in enumerate(scenario.choices):
            choice_btn = tk.Button(
                choices_frame,
                text=f"{i+1}. {choice.text}",
                font=self.body_font,
                fg=self.colors['text_primary'],
                bg=self.colors['bg_medium'],
                activebackground=self.colors['bg_light'],
                activeforeground=self.colors['text_primary'],
                relief=tk.FLAT,
                cursor="hand2",
                wraplength=700,
                justify=tk.LEFT,
                padx=20,
                pady=15,
                command=lambda c=choice: self.make_choice(c)
            )
            choice_btn.pack(pady=10, fill=tk.X, padx=20)
            choice_btn.bind('<Enter>', lambda e, b=choice_btn: b.configure(bg=self.colors['bg_light']))
            choice_btn.bind('<Leave>', lambda e, b=choice_btn: b.configure(bg=self.colors['bg_medium']))

    def make_choice(self, choice):
        """Process the player's choice"""
        self.choices_made.append({
            'scenario': self.scenarios[self.current_scenario_index].title,
            'choice': choice.text,
            'integrity_change': choice.integrity_change
        })

        # Update integrity score
        self.integrity_score = max(0, min(100, self.integrity_score + choice.integrity_change))

        # Show outcome
        self.show_outcome(choice)

    def show_outcome(self, choice):
        """Show the outcome of the choice"""
        self.clear_frame()
        self.current_state = GameState.OUTCOME

        scenario = self.scenarios[self.current_scenario_index]

        # Header
        header_frame = tk.Frame(self.main_frame, bg=self.colors['bg_dark'])
        header_frame.pack(fill=tk.X)

        tk.Label(
            header_frame,
            text="OUTCOME",
            font=self.subtitle_font,
            fg=self.colors['warning'],
            bg=self.colors['bg_dark']
        ).pack(side=tk.LEFT)

        # Integrity change indicator
        change_color = self.colors['success'] if choice.integrity_change > 0 else self.colors['danger']
        change_text = f"+{choice.integrity_change}" if choice.integrity_change > 0 else str(choice.integrity_change)

        tk.Label(
            header_frame,
            text=f"Integrity: {self.integrity_score}/100 ({change_text})",
            font=self.body_font,
            fg=change_color,
            bg=self.colors['bg_dark']
        ).pack(side=tk.RIGHT)

        # Your choice
        choice_frame = tk.Frame(self.main_frame, bg=self.colors['bg_light'], padx=15, pady=10)
        choice_frame.pack(pady=10, fill=tk.X)

        tk.Label(
            choice_frame,
            text="Your choice:",
            font=self.button_font,
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_light']
        ).pack(anchor='w')

        tk.Label(
            choice_frame,
            text=choice.text,
            font=self.body_font,
            fg=self.colors['text_primary'],
            bg=self.colors['bg_light'],
            wraplength=700,
            justify=tk.LEFT
        ).pack(anchor='w', pady=5)

        # Outcome text
        outcome_frame = tk.Frame(self.main_frame, bg=self.colors['bg_medium'], padx=15, pady=15)
        outcome_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Scrollable outcome
        canvas = tk.Canvas(outcome_frame, bg=self.colors['bg_medium'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(outcome_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_medium'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        tk.Label(
            scrollable_frame,
            text=choice.outcome_text,
            font=self.body_font,
            fg=self.colors['text_primary'],
            bg=self.colors['bg_medium'],
            justify=tk.LEFT,
            wraplength=700
        ).pack(pady=10, padx=10)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Continue button
        if self.current_scenario_index < len(self.scenarios) - 1:
            self.create_button(
                self.main_frame,
                "Continue to Next Scenario",
                self.next_scenario,
                self.colors['success']
            ).pack(pady=20)
        else:
            self.create_button(
                self.main_frame,
                "See Final Results",
                self.show_game_over,
                self.colors['accent']
            ).pack(pady=20)

    def next_scenario(self):
        """Move to next scenario"""
        self.current_scenario_index += 1
        self.show_scenario_intro()

    def get_integrity_color(self):
        """Get color based on integrity score"""
        if self.integrity_score >= 80:
            return self.colors['success']
        elif self.integrity_score >= 60:
            return self.colors['warning']
        elif self.integrity_score >= 40:
            return '#ff9800'  # Orange
        else:
            return self.colors['danger']

    def get_final_rank(self):
        """Get final rank based on integrity score"""
        if self.integrity_score >= 80:
            return (
                "EXEMPLARY OFFICER",
                """You represent the best of what law enforcement can be. Through every
challenge, you maintained your integrity while showing compassion and wisdom.

You understand that the badge is a responsibility, not a privilege. You've
proven that doing the right thing - even when it's hard - is what makes
a true officer of the law.

T.O. Martinez's Final Evaluation: "In all my years on the force, I've
trained a lot of rookies. You're one of the rare ones who came in with
character and left with even more. The LAPD is lucky to have you.
Welcome to the family, Officer."

Your journey is just beginning - and it's going to be remarkable.""",
                self.colors['success']
            )
        elif self.integrity_score >= 60:
            return (
                "GOOD OFFICER",
                """You've shown that you have the heart of a true officer. While you've
made some missteps along the way, you've learned from them.

The job is hard, and nobody gets it right every time. What matters is that
you kept trying to do better, to be better.

T.O. Martinez's Final Evaluation: "You've got potential, rookie. Real
potential. You made some calls I would have made differently, but you
never lost sight of why we do this job. Keep learning, keep growing.
You're going to be a solid cop."

The streets need officers like you who care enough to keep improving.""",
                self.colors['warning']
            )
        elif self.integrity_score >= 40:
            return (
                "STRUGGLING OFFICER",
                """The moral complexities of police work have tested you, and you've found
yourself on uncertain ground more than once.

This job forces us to make impossible choices. You haven't always chosen
wisely, but you haven't given up either.

T.O. Martinez's Final Evaluation: "I'm not going to sugarcoat it, rookie.
You've got some serious thinking to do about what kind of cop you want to
be. The potential is there, but so are some concerning patterns. My
recommendation: more training, more mentorship, and a hard look in the
mirror. The badge can make you a hero or a villain - you decide which."

The question is: will you learn from these experiences?""",
                '#ff9800'
            )
        else:
            return (
                "COMPROMISED OFFICER",
                """Somewhere along the way, you lost sight of why you put on the uniform.
The choices you made have compromised not just your integrity, but the
trust that the community places in officers.

T.O. Martinez's Final Evaluation: "I don't know what to tell you. You
came in with the same training as everyone else, but the choices you made...
This job isn't for everyone. Maybe you should think about whether this is
really your calling. Because right now? I wouldn't trust you to have my
back out there."

It's not too late to change. But first, you have to want to.""",
                self.colors['danger']
            )

    def show_game_over(self):
        """Show final game results"""
        self.clear_frame()
        self.current_state = GameState.GAME_OVER

        rank_title, rank_text, rank_color = self.get_final_rank()

        # Final Results header
        tk.Label(
            self.main_frame,
            text="FINAL EVALUATION",
            font=self.title_font,
            fg=self.colors['accent'],
            bg=self.colors['bg_dark']
        ).pack(pady=20)

        # Score display
        score_frame = tk.Frame(self.main_frame, bg=self.colors['bg_light'], padx=30, pady=20)
        score_frame.pack(pady=10)

        tk.Label(
            score_frame,
            text=f"Final Integrity Score: {self.integrity_score}/100",
            font=self.subtitle_font,
            fg=rank_color,
            bg=self.colors['bg_light']
        ).pack()

        tk.Label(
            score_frame,
            text=rank_title,
            font=self.title_font,
            fg=rank_color,
            bg=self.colors['bg_light']
        ).pack(pady=10)

        # Rank description
        desc_frame = tk.Frame(self.main_frame, bg=self.colors['bg_medium'], padx=20, pady=20)
        desc_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(desc_frame, bg=self.colors['bg_medium'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(desc_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_medium'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        tk.Label(
            scrollable_frame,
            text=rank_text,
            font=self.body_font,
            fg=self.colors['text_primary'],
            bg=self.colors['bg_medium'],
            justify=tk.LEFT,
            wraplength=700
        ).pack(pady=10, padx=10)

        # Choice summary
        tk.Label(
            scrollable_frame,
            text="\n--- YOUR CHOICES ---",
            font=self.button_font,
            fg=self.colors['warning'],
            bg=self.colors['bg_medium']
        ).pack(pady=10)

        for choice_data in self.choices_made:
            change = choice_data['integrity_change']
            change_text = f"+{change}" if change > 0 else str(change)
            change_color = self.colors['success'] if change > 0 else self.colors['danger']

            choice_text = f"{choice_data['scenario']}\n{choice_data['choice']} [{change_text}]"
            tk.Label(
                scrollable_frame,
                text=choice_text,
                font=self.body_font,
                fg=change_color,
                bg=self.colors['bg_medium'],
                justify=tk.LEFT,
                wraplength=650
            ).pack(pady=5, anchor='w')

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Buttons
        button_frame = tk.Frame(self.main_frame, bg=self.colors['bg_dark'])
        button_frame.pack(pady=20)

        self.create_button(
            button_frame,
            "Play Again",
            self.start_new_game,
            self.colors['success']
        ).pack(side=tk.LEFT, padx=10)

        self.create_button(
            button_frame,
            "Main Menu",
            self.show_main_menu,
            self.colors['bg_light']
        ).pack(side=tk.LEFT, padx=10)


def main():
    """Main entry point"""
    root = tk.Tk()

    # Center window on screen
    window_width = 900
    window_height = 700
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    # Set minimum size
    root.minsize(800, 600)

    game = RookiePuzzleGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
