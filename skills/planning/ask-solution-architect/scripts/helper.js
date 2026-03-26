/**
 * Helper scripts for ask-solution-architect
 */

module.exports = {
  /**
   * Evaluates a problem statement and suggests the appropriate framework routing.
   * This logic maps to the instructions in SKILL.md.
   */
  suggestFramework: (statement) => {
    const text = statement.toLowerCase();
    
    // Modification or Refactoring
    if (text.includes('refactor') || text.includes('modify') || text.includes('improve')) {
      return 'SCAMPER';
    }
    
    // Assessment or Risk Strategy
    if (text.includes('risk') || text.includes('strategy') || text.includes('audit')) {
      return 'SIX_HATS';
    }
    
    // Product Design or Ground-up builds
    return 'DESIGN_THINKING';
  }
};
