import { render, screen, fireEvent } from '@testing-library/react';
import NPCModal from '../NPCModal';
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

describe('NPCModal', () => {
  test('renders nothing when closed', () => {
    render(
      <NPCModal 
        npc={mockNPC} 
        isOpen={false} 
        onClose={() => {}} 
      />
    );
    
    expect(screen.queryByText('Description')).not.toBeInTheDocument();
  });

  test('renders full NPC details when open', () => {
    render(
      <NPCModal 
        npc={mockNPC} 
        isOpen={true} 
        onClose={() => {}} 
      />
    );
    
    // Check all major sections are present
    expect(screen.getByText('TEST ACE')).toBeInTheDocument();
    expect(screen.getByText('Description')).toBeInTheDocument();
    expect(screen.getByText('Test description')).toBeInTheDocument();
    expect(screen.getByText('Tactics')).toBeInTheDocument();
    expect(screen.getByText('Test tactics')).toBeInTheDocument();
  });

  test('calls onClose when close button is clicked', () => {
    const handleClose = jest.fn();
    render(
      <NPCModal 
        npc={mockNPC} 
        isOpen={true} 
        onClose={handleClose} 
      />
    );
    
    fireEvent.click(screen.getByRole('button', { name: /close/i }));
    expect(handleClose).toHaveBeenCalled();
  });
}); 