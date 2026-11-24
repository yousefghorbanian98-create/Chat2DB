// EXAMPLE, not an enabled or validated product gate. Run from mp-app/studio.
// Existing Studio has src/pages; do NOT invent src/features/* to satisfy rules.
// Positive/negative controls must prove coverage before this is made blocking.
module.exports = {
  forbidden: [
    {
      name: 'no-circular-browser-imports',
      severity: 'error',
      from: { path: '^src/' },
      to: { circular: true },
    },
    {
      name: 'no-node-core-in-browser',
      severity: 'error',
      from: { path: '^src/' },
      to: { dependencyTypes: ['core'] },
    },
    {
      name: 'no-electron-in-browser',
      severity: 'error',
      from: { path: '^src/' },
      to: { path: '(^|/)electron(/|$)' },
    },
  ],
  options: {
    doNotFollow: { path: 'node_modules' },
    tsConfig: { fileName: 'tsconfig.json' },
    enhancedResolveOptions: {
      exportsFields: ['exports'],
      conditionNames: ['import', 'browser', 'default'],
    },
  },
};
