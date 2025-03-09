# 檢查用戶是否在存在在資料庫中
if user_info_table.count_documents({'userid': json_body['source']['userId']}):