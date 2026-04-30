# UI & Design System

AgriX is built to feel like an Apple-level trillion-dollar consumer product applied to enterprise agriculture. It is designed for everyday operators, requiring high legibility and psychological trust.

## Core Principles
- **Light-Mode First:** Clean, airy, and high-contrast for readability in bright sunlight (in the field).
- **Psychology of Color:** Utilizing calming emeralds (`#10b981`), warm whites, and deep earthy slates to induce a feeling of safety, predictability, and growth.
- **Glassmorphism:** Strategic use of `backdrop-blur-xl` and semi-transparent backgrounds to create depth over complex data views.
- **Micro-Animations:** Use Framer Motion for non-blocking, subtle state transitions (hover, click, load) to make the UI feel alive.

## Component Rules
- **Modals & Overlays:** Must include a blurred backdrop.
- **Data Loading:** Never show a blank screen. Use `<Skeleton />` components that mirror the final shape of the data.
- **Colors:** Stick strictly to the defined CSS variables in `index.css`. Avoid hardcoding hex values.
