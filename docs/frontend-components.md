# Frontend layout rules

The site is rebuilt from measured source values, but its templates and CSS are
component-based. New pages must reuse the structures below instead of adding
page-specific copies of widths and spacing.

## Page flow

- `base.html` owns the header-to-content gap through `.site-main` and
  `--content-start-gap`. Individual pages must not compensate for the floating
  header contact card.
- A full-width page section is a direct child of `.site-main`.
- `.content-shell` is the shared 1200 px text/content width with 30 px minimum
  viewport gutters.
- `.layout-row` is the shared 1248 px builder row. Put it inside a section that
  provides its own 30 px horizontal padding.
- `.section-transition` is the standard 21 px boundary between major sections.

## Reusable components

- Use `components/section_heading.html` for major section headings and their
  yellow line.
- Use `components/parallax_banner.html` for every full-width parallax banner;
  pass only its background modifier and translated text.
- Use `components/feature_card.html` inside `.feature-grid` for image, title,
  body and action groups.
- Add `.feature-grid--three` for three equal cards; the mobile breakpoint still
  collapses the shared grid to one column.
- Use `.button`, a visual modifier such as `.button--primary`, and
  `.button__icon`; do not restyle links independently per card.
- Add `data-parallax` and `data-parallax-velocity` to sections that use the
  shared parallax behavior in `static/js/site.js`; do not create page-specific
  scroll handlers.
- Content images keep their intrinsic aspect ratio and fill the card width.
- Text visible to visitors must use `{% translate %}` and values from the
  translation tables. Ukrainian is the source language.

## Responsive behavior

- The desktop reference viewport is 1700 px wide.
- At 760 px and below, `.feature-grid` becomes one column and card side padding
  is removed. Section gutters still remain 30 px.
- Do not set card heights. Shared margins and real content determine the row
  height so German and Ukrainian can wrap safely.
- Validate every new component at 1700 px and 390 px, in both languages and in
  every interactive state.

## Assets and CSS

- Keep source assets local under `static/`; do not hotlink WordPress.
- Do not use inline style attributes or selectors based on page order such as
  `:nth-child()` for layout.
- Add spacing to the owning component. Pages compose components and must not
  repeat their internal measurements.
