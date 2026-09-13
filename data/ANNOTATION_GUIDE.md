# Golden-set annotation guide

## Goal
Label the **primary support intent** and whether the case is safe to auto-handle. Use only the customer message, not model predictions.

## Taxonomy
- `battery_charging`: battery drain, charging, heat during normal charging.
- `ios_update_performance`: slowdown, freezes, crashes, regressions tied to iOS updates.
- `network_connectivity`: cellular, Wi-Fi, Bluetooth, hotspot.
- `apple_id_account`: login, password, verification, account recovery.
- `app_store_purchases`: purchases, refunds, duplicate charges, payment method, App Store downloads.
- `icloud_backup_storage`: backup, iCloud storage/sync/restore, possible cloud data loss.
- `device_hardware_damage`: physical damage/failure, water, swelling, camera/button hardware.
- `audio_calls_media`: calls, speaker/mic, Apple Music/AirPods.
- `keyboard_messaging`: keyboard/autocorrect/iMessage/Messages.
- `general_other`: unclear/general complaint or unsupported issue.

## Escalation
Mark `true` for account-specific access, billing/refunds, potential data loss, hardware/safety inspection, fraud/PII, or ambiguity.

## Sampling protocol
1. Filter Kaggle `twcs.csv` to inbound messages in AppleSupport threads.
2. Deduplicate near-identical messages.
3. Build rough topic buckets to avoid a battery/iOS-only set.
4. Randomly sample with seed 42.
5. Label without seeing model output.
6. Mark ambiguous rows and adjudicate after labelling.
