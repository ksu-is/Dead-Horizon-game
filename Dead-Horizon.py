# Dead Horizon - Text Based Zombie Apocalypse Survival Game
import json
import os
import random
from dataclasses import dataclass, field, asdict

# Config & Balancing

Sectors_To_Evac = 20        # reach this many sectors to get to evacuation
Move_Sectors_Range = (1,3)  # number of sectors you move when relocating
Survivor_Size_Range = (2,5)

Initial_Supplies = {'food': 200, 'water': 150, 'medkits': 3, 'antivirals': 3, 'materials': 15, 'ammo': 40}

Consumption_Per_Survivor_Per_Day = {'food': 2, 'water': 2}

Base_Max_Integrity = 10
Rest_Heal = 1
Fortify_Boost = (1,3)
Max_Health = 10

Horde_Base_Chance = 0.18
Infection_Tick_Chance = 0.10
Good_Event_Chance = 0.17
Raider_Chance = 0.12

Save_File = "Dead-Horizon_save.json"

# Data Models

@dataclass
class Survivor:
    name: str
    health: int = Max_Health
    alive: bool = True
    infected: bool = False  # if infected is True, the infection advances daily until it is treated

    def damage(self, amount: int):
        if not self.alive:
            return
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.alive = False
    
    def heal(self, amount: int):
        if not self.alive:
            return
        self.health = min(Max_Health, self.health + amount)

@dataclass
class GameState:
    day: int = 1
    sector: int = 0
    sectors_to_evac: int = Sectors_To_Evac
    supplies: dict = field(default_factory = lambda: Initial_Supplies.copy())
    base_integrity: int = Base_Max_Integrity
    squad: list = field(default_factory = list)
    morale: int = 5
    game_over: bool = False
    
    def squad_alive(self):
        return [s for s in self.squad if s.alive]
    
    def anyone_alive(self):
        return any(s.alive for s in self.squad)
    
    def evac_reached(self):
        return self.sector >= self.sectors_to_evac
    
    def base_breached(self):
        return self.base_integrity <= 0
    
    # Utilities

    def clamp(n, lo, hi):
        return max(lo, min(hi,n))
    
    def safe_int(s, default):
        try:
            return int(s)
        except:
            return default
    
    def prompt_choice(prompt, choices):
        while True:
            for p, c in choices.items():
                print(f" [{p}] {c}")
            sel = input("> ").strip().lower()
            if sel in choices:
                return sel
            print("Invalid choice.\n")

    # Save/Load Functionality

    def save_game