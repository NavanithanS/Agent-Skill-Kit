---
name: flutter-architect
description: Senior Flutter skill using FVM. Enforces project-specific standards: Provider, Layer-First Architecture, Stream-based Services, and strict coding conventions.
---

## 1. FVM & Version Control Protocol
**CRITICAL:** Do NOT use the global `flutter` command.
1.  **Check Configuration:** Look for `.fvmrc` or `.fvm/fvm_config.json` in the root.
2.  **Enforce Version:**
    *   **Command:** ALWAYS use `fvm flutter <command>`.
    *   **Verification:** Before starting, run `fvm flutter --version` and match it against the version defined in `.fvmrc`.
    *   **Setup:** If FVM is not configured, run `fvm install <version>` then `fvm use <version>`.

## 2. Project Architecture Standards

### A. Folder Structure (Layer-First)
Do NOT use Feature-First. Adhere to the existing **Layer-First** structure:
```text
lib/
├── api/                     # Retrofit API clients and models
│   ├── models/             # Auto-generated json_serializable models
│   └── *_api.dart          # Retrofit interfaces
├── components/             # Reusable UI widgets
├── screens/                # Screens organized by feature area
│   ├── tabs/              # Main bottom nav screens
│   ├── auth/              # Auth screens
│   └── ...
├── constants.dart          # App-wide constants/theme
└── *Service.dart          # Core business logic (Singleton Services)
```

### B. State Management (Streams + Provider)
The project uses a hybrid approach. Do NOT introduce Riverpod or Bloc.
1.  **Business Logic:** Use **Singleton Services** (e.g., `AuthService`, `CartService`).
    *   Expose state changes via **Streams** (`StreamController.broadcast`).
    *   Services handle API calls and data processing.
2.  **UI binding:**
    *   Use `StreamSubscription` in `StatefulWidget` to listen to service events.
    *   Use `Provider` (minimal usage) specifically for injecting dependencies or simple UI state synchronization at the root.

### C. API & Code Generation
1.  **Retrofit:** Define APIs in `lib/api/*_api.dart`.
2.  **Models:** Use `json_serializable` in `lib/api/models/`.
3.  **Generation:** ALWAYS run this after modifying models/APIs:
    ```bash
    fvm flutter pub run build_runner build
    ```

### D. Navigation
Use standard **Navigator 1.0**.
1.  **Routes:** Defined in `onGenerateRoute` in `main.dart`.
2.  **Tabs:** Managed by `BottomTabNavigation` (or similar main wrapper).
3.  **Navigation:** `Navigator.of(context).pushNamed(...)`.

## 3. Coding Standards & Best Practices

### A. Extensions & Formatting
Use the simplified extensions from `lib/components/Utils.dart` instead of manual formatting.
*   **Currency:** `price.currency` (e.g., `100.currency` → "RM 100.00")
*   **Dates:** `date.shortDate`, `date.longDate`, `date.timeago`.
*   **Strings:** `str.capitalize`.

### B. Navigation Key
For navigation without a context (e.g., inside Services), use the global key:
```dart
import 'package:storeapp/components/Utils.dart';
// ...
navKey.currentState?.pushNamed(...);
```

### C. Error Handling
1.  **User Feedback:** Use `showMessage(context, ...)` from `Dialogs.dart` for alerts/snackbars.
2.  **Crashlytics:** Report non-fatal errors explicitly:
    ```dart
    FirebaseCrashlytics.instance.recordError(error, stack, fatal: false);
    ```

### D. Linting
Adhere strictly to `flutter_lints` rules defined in `analysis_options.yaml`. Run `fvm flutter analyze` to verify.

## 4. Development Workflow
1.  **Analysis:** Run `fvm flutter analyze` regularly.
2.  **Testing:** Run `fvm flutter test` for unit tests.
3.  **Builds:** Use the provided scripts:
    *   Android: `./ship-android.sh`
    *   iOS: `./ship-ios.sh`

## Trigger Phrases

Activate this skill when the user says things like:
- "Set up a Flutter screen"
- "Create a new service in Flutter"
- "Architect this Flutter app"
- "How should I manage state here?"

