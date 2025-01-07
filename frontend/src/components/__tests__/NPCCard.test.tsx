import { render, screen, fireEvent } from '@testing-library/react';
import NPCCard from '../NPCCard';
import { NPC } from '../../types';

const mockNPC: NPC = {
  name: "TEST ACE",
  role: "striker",
  tier: 2,
  description: "Test description",
  tactics: "Test tactics",
  stats: {
    hp: 12,
    armor: 0,
    evade: 15,
    edef: 8,
    heatcap: 8,
    speed: 6,
    sensor: 10,
    save: 12,
    hull: -2,
    agility: 4,
    systems: 2,
    engineering: 1,
    size: [1],
    activations: 1
  },
  features: {
    base: ["Test Base Feature 1", "Test Base Feature 2"],
    optional: ["Test Optional Feature"]
  }
};

describe('NPCCard', () => {
  test('renders basic NPC information', () => {
    render(<NPCCard npc={mockNPC} />);
    
    expect(screen.getByText('TEST ACE')).toBeInTheDocument();
    expect(screen.getByText('striker')).toBeInTheDocument();
    expect(screen.getByText('Tier 2')).toBeInTheDocument();
  });

  test('renders stats correctly', () => {
    render(<NPCCard npc={mockNPC} />);
    
    expect(screen.getByText('12')).toBeInTheDocument(); // HP
    expect(screen.getByText('0')).toBeInTheDocument();  // Armor
    expect(screen.getByText('15')).toBeInTheDocument(); // Evade
    expect(screen.getByText('8')).toBeInTheDocument();  // E-Def
  });

  test('shows modal when clicking Show Details button', () => {
    render(<NPCCard npc={mockNPC} />);
    
    const button = screen.getByText('Show full details');
    fireEvent.click(button);
    
    // Modal content should be visible
    expect(screen.getByText('Description')).toBeInTheDocument();
    expect(screen.getByText('Test description')).toBeInTheDocument();
    expect(screen.getByText('Tactics')).toBeInTheDocument();
    expect(screen.getByText('Test tactics')).toBeInTheDocument();
  });

  test('closes modal when clicking close button', () => {
    render(<NPCCard npc={mockNPC} />);
    
    // Open modal
    fireEvent.click(screen.getByText('Show full details'));
    
    // Close modal
    fireEvent.click(screen.getByRole('button', { name: /close/i }));
    
    // Modal content should not be visible
    expect(screen.queryByText('Description')).not.toBeInTheDocument();
  });
}); 