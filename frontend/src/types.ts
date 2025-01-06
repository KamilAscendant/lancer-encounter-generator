export interface NPC {
  name: string;
  role: string;
  tier: number;
  description: string;
  tactics: string;
  stats: {
    hp: number;
    armor: number;
    evade: number;
    edef: number;
    heatcap: number;
    speed: number;
    sensor: number;
    save: number;
    hull: number;
    agility: number;
    systems: number;
    engineering: number;
    size: number[];
    activations: number;
  };
  features: {
    base: string[];
    optional: string[];
  };
}

export interface Encounter {
  number_of_players: number;
  player_level: number;
  tier: number;
  number_of_npcs: number;
  npcs_by_role: Record<string, NPC[]>;
}