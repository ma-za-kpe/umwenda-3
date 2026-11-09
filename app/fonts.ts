// Self-hosted faces (owner decision D2): the pinned @fontsource packages are
// bundled into the export, so no font loads from elsewhere. The design system
// writes this file from the brand's type pairing; only faces the template pins
// may be imported here (tests/stack_policy.py). Until it does, the template
// imports none: its tokens use the system faces as neutral placeholders (#326).
export {};
