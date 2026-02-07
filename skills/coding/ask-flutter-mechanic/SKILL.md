---
name: ask-flutter-mechanic
description: Flutter maintenance with FVM. Clean builds, iOS/Android fixes, asset generation, release.
triggers: ["clean flutter build", "fix ios build", "resolve dependencies", "prepare flutter release"]
---

<critical_constraints>
❌ NO global `flutter` → always `fvm flutter`
❌ NO skipping build_runner after model changes
✅ MUST check `.fvmrc` version matches `fvm flutter --version`
✅ MUST run `bundle exec pod install` not raw `pod install`
</critical_constraints>

<health_check>
1. Read `.fvmrc` (e.g., 3.35.5)
2. Run `fvm flutter --version` to verify
3. Run `fvm flutter doctor`
</health_check>

<clean_build>
```bash
fvm flutter clean
fvm flutter pub get
fvm flutter pub run build_runner build --delete-conflicting-outputs
```
</clean_build>

<ios_fix>
Trigger: CocoaPods errors, linker failures
```bash
cd ios
bundle install
rm -rf Pods Podfile.lock
bundle exec pod install --repo-update
cd ..
```
</ios_fix>

<android_fix>
Trigger: Gradle errors, SDK mismatch
- Check `android/gradle/wrapper/gradle-wrapper.properties`
- Run `./gradlew clean` inside android/
</android_fix>

<assets>
- Icons: `fvm dart run flutter_launcher_icons`
- Splash: `fvm dart run flutter_native_splash:create`
</assets>

<release>
- Android: `./ship-android.sh` (runs fastlane release)
- iOS: `./ship-ios.sh` (runs fastlane deploy)
Prereqs: key.properties (Android), certificates (iOS)
</release>

<dependency_conflict>
1. Read conflict tree in terminal
2. `fvm flutter pub upgrade <package_name>`
3. Check pubspec.lock for changes
</dependency_conflict>
