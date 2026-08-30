import js from '@eslint/js';
import reactHooks from 'eslint-plugin-react-hooks';
import reactRefresh from 'eslint-plugin-react-refresh';
import tseslint from 'typescript-eslint';

/**
 * FINN-LOOP Phase 3 quality gate. The numeric limits below are the loop's own
 * contract (file <= 300 lines, function <= 50 lines, <= 3 params), and the
 * security/type rules are hard errors, not warnings: the gate is "0 warnings".
 */
export default tseslint.config(
  {
    ignores: ['dist/**', 'coverage/**', 'node_modules/**', 'electron/**'],
  },
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    files: ['**/*.{ts,tsx}'],
    plugins: {
      'react-hooks': reactHooks,
      'react-refresh': reactRefresh,
    },
    rules: {
      ...reactHooks.configs.recommended.rules,
      'react-refresh/only-export-components': ['warn', { allowConstantExport: true }],

      // Loop contract: no escape hatches from the type system.
      '@typescript-eslint/no-explicit-any': 'error',
      '@typescript-eslint/ban-ts-comment': 'error',
      '@typescript-eslint/no-unused-vars': [
        'error',
        { argsIgnorePattern: '^_', varsIgnorePattern: '^_' },
      ],
      '@typescript-eslint/consistent-type-imports': [
        'error',
        { prefer: 'type-imports', fixStyle: 'inline-type-imports' },
      ],

      // Loop contract: never swallow an error silently.
      'no-empty': ['error', { allowEmptyCatch: false }],
      'no-console': 'error',

      // Loop contract: size limits.
      'max-lines': ['error', { max: 300, skipComments: true, skipBlankLines: true }],
      'max-lines-per-function': ['error', { max: 50, skipComments: true, skipBlankLines: true }],
      'max-params': ['error', { max: 3 }],
      'max-depth': ['error', { max: 4 }],

      eqeqeq: ['error', 'always'],
    },
  },
  {
    // The service worker runs in its own global scope (self/caches/clients).
    files: ['public/sw.js'],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'script',
      globals: {
        self: 'readonly',
        caches: 'readonly',
        clients: 'readonly',
        fetch: 'readonly',
        URL: 'readonly',
        Promise: 'readonly',
        CustomEvent: 'readonly',
      },
    },
  },
  {
    // Tests exercise failure paths on purpose; keep the limits off there.
    files: ['**/*.test.{ts,tsx}'],
    rules: {
      'max-lines': 'off',
      'max-lines-per-function': 'off',
      '@typescript-eslint/no-unsafe-assignment': 'off',
    },
  },
);
