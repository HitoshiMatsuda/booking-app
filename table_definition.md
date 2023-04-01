# テーブル設計(DB定義書)
グラウンド（施設）予約システムのテーブル定義を記載する。

## table_users
_user_id:ユーザーID
user_id:1
_user_name:ユーザー名
user_name:松田仁志
_user_rank:ユーザーランク
user_rank:1

##　table_institutions
_institution_id:施設ID
institution_id:1
_institution_name:施設ID
institution_name:駒沢オリンピック公園
_institution_capacity:施設ID
institution_capacity:100
_institution_starttime:利用可の時間（開始）
institution_starttime:08:00
_institution_endtime:利用可の時間（終了）
institution_endtime:20:00

## table_bookings
_booking_id:（予約ID）
booking_id:1
_user_id:（予約者ID）
user_id:1
_institution_id:（予約ID）
institution_id:1
_riservation_number:（予約人数）
riservation_number:50
_date:（予約日）
date:2023/03/01
_start:（利用開始時間）
start:10:00
_end:（利用終了時間）
end:18:00

## CRUD操作一覧
### CREATE
* ユーザー情報登録
* 施設登録
* 予約登録

### READ
* ユーザー情報読み込み
* 施設読み込み
* 予約読み込み

### UPDATE
* なし

### DELETE
* なし
