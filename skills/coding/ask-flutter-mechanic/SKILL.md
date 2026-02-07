---
name: flutter-mechanic
description: Maintenance skill for Flutter projects using FVM. Handles clean builds, iOS/Android specific fixes, asset generation, and release protocols.
---

## 1. Version Control & Health
**Always Start Here:**
1.  **Check Version:** Read `.fvmrc` (e.g., `3.35.5`) and ensure match with `fvm flutter --version`.
2.  **Doctor:** Run `fvm flutter doctor` to check environment health.

## 2. The "Clean Build" Protocol
**Trigger:** Build failures, weird UI glitches, or "API code not generated".

### Step A: The FVM Clean
1.  `fvm flutter clean`
2.  `fvm flutter pub get`
3.  `fvm flutter pub run build_runner build --delete-conflicting-outputs`
    *   *Critical:* This regenerates `json_serializable` and `retrofit` code.

### Step B: iOS Specifics (`ios/` folder)
**Trigger:** "CocoaPods not found" or "Linker command failed".
1.  `cd ios`
2.  **Fastlane/Ruby:** `bundle install` (Ensure Fastlane and Pods dependencies are aligned).
3.  **Nuclear Clean:** `rm -rf Pods Podfile.lock`
4.  **Reinstall:** `bundle exec pod install --repo-update` (Preferred over raw `pod install`).
5.  `cd ..`

### Step C: Android Specifics (`android/` folder)
**Trigger:** Gradle errors or SDK version mismatches.
1.  Check `android/gradle/wrapper/gradle-wrapper.properties` distribution URL.
2.  Sync Gradle via Android Studio or run `./gradlew clean` inside `android/`.

## 3. Project Asset Maintenance
**Trigger:** Updates to `pubspec.yaml` assets or configuration.

*   **App Icons:** `fvm dart run flutter_launcher_icons`
*   **Splash Screens:** `fvm dart run flutter_native_splash:create`

## 4. Release Protocols ("The Ship It List")
**Precautions:** Ensure `key.properties` exists (Android) and Certificates are installed (iOS).

### A. Android Release
**Script:** `./ship-android.sh`
*   **Actions:** Enters `android/`, runs `fastlane release`.
*   **Output:** Uploads AAB to Play Store Console.

### B. iOS Release
**Script:** `./ship-ios.sh`
*   **Actions:** Enters `ios/`, runs `fastlane deploy`.
*   **Output:** Uploads IPA to TestFlight/App Store Connect.

## 5. Dependency Conflict Resolution
**Scenario:** `pub get` fails.
1.  **Analyze:** Read the conflict tree in the terminal.
2.  **Unlock:** `fvm flutter pub upgrade <package_name>` to update transitive dependencies.
3.  **Verify:** Check `pubspec.lock` for changes.

## Trigger Phrases

Activate this skill when the user says things like:
- "Clean build my Flutter app"
- "Fix iOS build errors"
- "Resolve dependency conflicts"
- "Prepare this app for release"

