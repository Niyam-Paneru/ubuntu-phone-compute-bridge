# Invariants

1. **Work is selected by reviewed job name, not arbitrary command text.**
2. **Remote failure never silently becomes local success.**
3. **The returned job identity must match the requested job.**
4. **The returned execution location must match the expected worker.**
5. **Artifact integrity is checked separately from job success.**
6. **Transport identity changes are stop conditions.**

The phone is allowed to fail. The controller is not allowed to lie about where the work ran.
