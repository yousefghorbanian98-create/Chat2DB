import type { GodmodeAdapter } from '../adapters/godmode.ts'
import type { Skill } from '../types.ts'

/**
 * تبدیلِ دستورات و ساب‌ایجنت‌های Godmode به «skill» برای مسیریاب.
 * این همان نقطه‌ای است که لایهٔ Soup و لایهٔ Godmode به هم می‌رسند.
 *
 * فیلدِ examples از طراحی خودِ Soup آمده (مستندات: "Training phrases also
 * used for BM25 selection"). مثال‌ها از جدولِ Commands/Subagents در
 * SOURCE: https://github.com/patrickking67/godmode (Apache-2.0) استخراج شده‌اند.
 *
 * چرا examples لازم شد؟ بدون آن، سیگنالِ BM25 فقط روی description بود و
 * یک عبارتِ دوقسمتی (مانند "pull request") می‌توانست بر فعلِ قصد
 * (مانند "review") غلبه کند. مثال‌ها وزنِ قصد را برمی‌گردانند.
 */
const COMMAND_EXAMPLES: Record<string, string[]> = {
  revelation: [
    'explain this codebase',
    'how does this repository fit together',
    'map the architecture',
    'what does this project do',
  ],
  gospel: [
    'learn the conventions of this project',
    'document the coding standards',
    'what rules does this repo follow',
  ],
  prophecy: [
    'what should we build next',
    'plan the roadmap',
    'guide me on next steps',
    'which direction should we take',
  ],
  genesis: [
    'build a new feature end to end',
    'implement this from scratch',
    'scaffold a new module',
    'create the initial implementation',
  ],
  summon: [
    'which agent should handle this',
    'delegate this to a subagent',
    'spawn a specialist for this task',
  ],
  judgment: [
    'review this pull request',
    'review my code',
    'check this for blockers and bugs',
    'critique this change',
  ],
  sanctify: [
    'clean up the formatting',
    'lint and format the code',
    'tidy up this file',
    'normalize the style',
  ],
  exorcise: [
    'why is this test failing',
    'debug this bug',
    'find the root cause',
    'trace the source of this error',
  ],
  covenant: [
    'write a commit message for these changes',
    'prepare the commit',
    'summarize this branch for the changelog',
  ],
}

const AGENT_EXAMPLES: Record<string, string[]> = {
  oracle: ['recon the codebase', 'trace the data flow', 'map where this handler is defined'],
  demiurge: ['implement this well scoped feature', 'build this module'],
  inquisitor: ['audit this for security issues', 'find silent failures', 'rigorous review'],
  arbiter: ['run the project checks', 'do the tests pass', 'verify the build'],
  seer: ['root out the true cause of this bug', 'why does this test fail'],
}

export function buildSkills(godmode: GodmodeAdapter): Skill[] {
  const skills: Skill[] = []

  for (const c of godmode.listCommands()) {
    skills.push({
      name: c.slug,
      description: c.description || c.name,
      instructions: c.body,
      tags: ['command', c.slug],
      examples: COMMAND_EXAMPLES[c.slug] ?? [],
      source: c.source,
    })
  }

  for (const a of godmode.listAgents()) {
    skills.push({
      name: a.slug,
      description: a.description || a.name,
      instructions: a.body,
      tags: ['agent', a.slug],
      examples: AGENT_EXAMPLES[a.slug] ?? [],
      source: a.source,
    })
  }

  return skills
}
