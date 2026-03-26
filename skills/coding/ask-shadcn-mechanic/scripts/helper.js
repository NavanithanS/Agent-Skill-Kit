/**
 * Helper scripts for ask-shadcn-mechanic
 * Designed to perform regex pattern matching and structural validation.
 */

module.exports = {
  /**
   * Scans a JSX string for hardcoded arbitrary Tailwind colors that violate semantic theming.
   */
  hasHardcodedColors: (jsxString) => {
    const hardcodedColorsPattern = /\b(bg|text|border|ring)-(slate|gray|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)-\d{2,3}\b/g;
    return hardcodedColorsPattern.test(jsxString);
  },

  /**
   * Validates that standard semantic colors are being utilized.
   */
  usesSemanticColors: (jsxString) => {
    const semanticColorsPattern = /\b(bg|text|border)-(background|foreground|card|popover|primary|secondary|muted|accent|destructive)\b/g;
    return semanticColorsPattern.test(jsxString);
  },

  /**
   * Checks for inline styles which violate the <critical_constraints>.
   */
  hasInlineStyles: (jsxString) => {
    return /style=\{\{.*?\}\}/g.test(jsxString);
  },

  /**
   * Ensures the tailwind-merge util 'cn()' is present in className assignments.
   */
  usesCnUtility: (jsxString) => {
    return /className=\{cn\(.*?\)\}/g.test(jsxString);
  }
};
