---
name: ask-flutter-architect
description: Flutter scaffolding with FVM, Layer-First architecture, Streams+Provider state.
triggers: ["flutter screen", "create flutter service", "architect flutter app", "manage state flutter"]
---

<critical_constraints>
❌ NO global `flutter` command → use `fvm flutter`
❌ NO Riverpod/Bloc → project uses Streams+Provider
❌ NO Feature-First folders → use Layer-First
✅ MUST verify FVM version matches `.fvmrc`
✅ MUST run `fvm flutter pub run build_runner build` after model changes
✅ MUST use extensions from `lib/components/Utils.dart`
</critical_constraints>

<fvm_protocol>
1. Check `.fvmrc` or `.fvm/fvm_config.json`
2. Run `fvm flutter --version` to verify
3. ALL commands: `fvm flutter <command>`
</fvm_protocol>

<folder_structure>
lib/
├── api/              # Retrofit clients + models
├── components/       # Reusable UI widgets
├── screens/          # Screens by feature (tabs/, auth/, ...)
├── constants.dart    # App-wide constants
└── *Service.dart     # Singleton business logic
</folder_structure>

<state_management>
- Business logic: Singleton Services with StreamController.broadcast
- UI binding: StreamSubscription in StatefulWidget
- Provider: minimal, for root-level dependency injection only
</state_management>

<api_pattern>
- Retrofit: `lib/api/*_api.dart`
- Models: `lib/api/models/` with json_serializable
- Generation: `fvm flutter pub run build_runner build`
</api_pattern>

<navigation>
- Navigator 1.0 with onGenerateRoute in main.dart
- Tabs via BottomTabNavigation wrapper
- Context-free: use `navKey.currentState?.pushNamed(...)`
</navigation>

<extensions>
price.currency → "RM 100.00"
date.shortDate, date.longDate, date.timeago
str.capitalize
</extensions>
