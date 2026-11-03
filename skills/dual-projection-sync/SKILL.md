---
name: dual-projection-sync
description: Keep specification, implementation, and tests synchronized as three co-equal projections of one normative contract, and reconstruct any missing projection. Use when implementing or changing features, writing code or tests, updating an intent/ specification, or auditing a repository for drift between spec, code, and tests. Recover code from spec+tests, tests from spec+code, or spec from code+tests.
license: MIT
---

# Dual-Projection Synchronization

## When to use

Activate this skill whenever you are about to, or are asked to:

- Implement a feature or change an existing behavior.
- Write, modify, or review a subsystem contract (an `intent/` specification).
- Write or update tests.
- Audit a repository for synchronization drift between specification, code, and tests.
- Reconstruct a missing projection (code, tests, or spec) from the other two.

Do **not** use it for tasks that touch none of the three realms, such as pure prose edits, dependency bumps with no behavioral change, or operations work outside the repository's contract surface.

## The model

Treat every behavior in the system as existing in **three realms**, and treat code and tests as *disposable, cached artifacts* of an evolving mental model that is made durable only by the specification.

1. **The Normative Specification (the emergent ideal).** A lean, strict corpus under `intent/`. It is the single source of truth for *what the system must do*. It describes active contracts only — observable behavior, invariants, boundaries, and acceptance criteria. It **excludes** roadmap items, meeting notes, changelogs, migration histories, and implementation details.
2. **The Dual Material Projections.** Implementation (code) and Verification (tests) are parallel, mutually mirroring expressions of the normative intent:
   - **Code** is the projection that makes behavior executable in production.
   - **Tests** are the projection that makes behavior falsifiable.
   - Neither is primary. Each is a co-equal rendering of the same underlying logic, and each must trace to the specification.
3. **The Recovery Axiom (mutually mirroring regeneration).** Because the projections are symmetric, any one can be regenerated from the other two (see "Regeneration" below).

### Directory layout

Treat these as defaults; adapt the names to the language and project, then state the mapping once at the top of your work.

```
intent/    Normative specification (active contracts, one file per subsystem)
src/       Implementation projection (code)
test/      Verification projection (tests)
```

## Rules of engagement

### 1. Atomic synchronization

Every behavioral modification must advance **all three realms in one synchronized unit of work**:

- Change to code ⟹ update the corresponding `intent/` entry **and** add/adjust the test that pins it.
- Change to a test ⟹ confirm the behavior is present in `intent/` **and** that the code either satisfies it or is being changed to.
- Change to `intent/` ⟹ update code and tests together, unless this is a valid specification-lead update (below).

Changing code without updating the specification or the tests is **structural drift** and is not shippable. A change that touches only two realms is a partial commit of the same change, not a finished change.

### 2. Valid asymmetry (specification-lead)

A **specification-only** update is permitted when its purpose is to sharpen the contract or set the architecture *before* implementation catches up — for example, stating a new invariant, tightening an acceptance criterion, or splitting a subsystem boundary.

Rules for specification-lead updates:

- Mark the change as leading: add an explicit `status: specified, not yet implemented` note or an equivalent marker so the drift is visible, never silent.
- Do not claim the behavior exists until code and tests follow in the next unit of work.
- Track the lag; a specification-lead update left unpaired indefinitely is still drift.

### 3. Exemptions

The following may bypass full three-realm synchronization:

- **Pure cosmetic styling** — visual changes with zero observable behavior difference (colors, spacing, layout that does not alter semantics). If a test asserts on it, it is no longer cosmetic.
- **Documentation wording fixes** — typo and clarity edits to prose that do not change a stated contract.
- **Permanent feature deprecation** — removing behavior for good. Update the specification to mark the contract *removed*, delete the code, and delete or invert the tests; never leave dead code or orphaned tests behind.

If an exemption is claimed and later turns out to have changed behavior, retroactively restore full synchronization.

## Agent agency and drift arbitration

### Authorized autonomy: projection synthesis

You are authorized to **generate** the missing projection when the other two are present and consistent:

- **Spec + Tests → Code:** implement exactly the behavior the tests demand, nothing more. For every decision not covered by spec or test, prefer the simplest choice and flag the ambiguity.
- **Spec + Code → Tests:** derive a test for each normative behavior. Assert observable outcomes, not implementation details. Write the test so it fails against the prior (legacy) state, proving it discriminates.
- **Code + Tests → Spec:** distill the joint behavior of code and tests into a declarative `intent/` entry. Exclude implementation detail. Every statement in the spec must map to at least one test.

### Prohibited: drift arbitration

When the dual projections **conflict** — a test fails against an implementation change, code diverges from the normative specification, or a test contradicts the spec — you are **strictly prohibited from guessing or auto-resolving**. Do not pick a winner, delete a "failing" test, or silently edit the spec to match the code.

Instead, **halt** and:

1. Name the divergence precisely: which realm says what, and where they disagree.
2. Reproduce the conflict with the smallest concrete evidence (a failing test, a spec quote vs. a code quote).
3. Present the options without choosing: (a) change the spec to reflect the new behavior, (b) change the code to satisfy the spec, or (c) adjust the test if it misstates the contract.
4. Flag for **human arbitration**. Do not proceed until the human resolves the intent.

The human owns the mental model; you own the projections. Only the human may change what the system is *supposed* to do.

## Regeneration

Reconstruct the missing projection using the symmetry of the other two. Work from the normative specification whenever it exists; it is authoritative over both projections.

### Spec + Tests → Code

1. Read every `intent/` entry for the subsystem and its tests.
2. Enumerate the observable behaviors and their acceptance criteria.
3. Implement the minimal code that satisfies every test and no spec-undeclared behavior.
4. Refuse to add logic a test cannot reach; if the spec implies behavior the tests do not cover, add the test first (atomic synchronization).
5. Flag any spec/tests disagreement as drift arbitration (above), not as an excuse to guess.

### Spec + Code → Tests

1. For each normative statement, write at least one test asserting the observable outcome.
2. Assert behavior through public interfaces; never assert internal structure.
3. Prove the test discriminates: run it against the *previous* code state and confirm it fails, then confirm it passes against the current implementation.
4. Cover the contract's boundaries and failure modes stated in the spec, not just the happy path.

### Code + Tests → Spec

1. Read code and tests together; ignore comments as a source of truth.
2. Extract the *observable* behavior the tests lock in, and the behavior the code exposes.
3. Write a declarative `intent/` entry: what the subsystem guarantees, its invariants, and its boundaries.
4. Strip all implementation detail (data structures, algorithms, file layout).
5. Verify bidirectionally: each spec statement maps to ≥1 test, and each test maps to ≥1 spec statement. Unmapped tests reveal either a missing contract or over-specified tests.

## Pre-commit / pre-merge self-audit

Before finalizing any unit of work, answer all of the following:

1. **Does the normative specification stand alone?** Could a new engineer read `intent/` and describe the behavior without reading code or tests? Is it free of roadmap items, changelog noise, and implementation detail?
2. **Do the verification tests fail against the legacy implementation state?** Have you proven each new/changed test discriminates by watching it fail before the fix and pass after?
3. **Does the implementation contain unmotivated logic?** Is there any branch, flag, default, or side effect not stated in the spec and not asserted by a test? If so, either remove it or document it in all three realms.
4. **Is every realm touched in this unit?** For each behavioral change, confirm spec, code, and tests all moved together — or that the change is a declared specification-lead update or an exemption.
5. **Is every spec statement traceable to a test, and vice versa?** Walk both directions and resolve orphans.
6. **Is there any unresolved drift?** If code and tests disagree, or code diverges from spec, you have not finished: halt and escalate per drift arbitration.

## Failure modes

- **Drift by omission** — code changed, test or spec left stale. Most common failure; catch it with the self-audit.
- **Spec rot** — `intent/` documents an idealized past, not the running system. Rebuild it from code + tests.
- **Test tautology** — tests mirror implementation instead of specification. Fix by asserting observable outcomes and proving they fail against a divergent state.
- **Silent arbitration** — guessing when projections conflict. Never resolve drift unilaterally; escalate.
- **Specification bloat** — roadmap, notes, and changelog leaking into `intent/`. Keep the corpus normative and lean.
- **Specification-lead lag** — a spec-only change that never gets paired. Track and close it in the next unit of work.
