import argparse
import os
import re


def what_is_the_filetype():
    """获取用户输入的文件类型，做非空校验"""
    while True:
        filetype = input("請輸入要處理的文件類型（如txt）：").strip().lower()
        if filetype:
            return filetype
        print("錯誤：文件類型不能為空！請重新輸入")

# ===================== 独立函数：基础校验 =====================
def validate_folder_and_files(folder, filetype):
    """
    驗證文件夾有效性
    :param folder: 文件夾路徑
    :param filetype: 文件類型（如txt）
    :return: 文件夹绝对路径（失敗返回None）
    """
    if not filetype:
        print("錯誤：文件類型不能為空！")
        return None

    folder_abs = os.path.abspath(folder)
    if not os.path.exists(folder_abs):
        print(f"錯誤：路徑 {folder_abs} 不存在！")
        return None

    return folder_abs

# ===================== 独立函数：檔案檢查 =====================
def check_files(folder_abs, filetype):
    """
    筛选指定类型的非隐藏文件
    :param folder_abs: 文件夹绝对路径
    :param filetype: 文件类型（如txt）
    :return: 有效文件绝对路径列表（失敗返回None）
    """
    file_paths = []
    for filename in os.listdir(folder_abs):
        if filename.endswith(f".{filetype}") and not filename.startswith("."):
            file_abs = os.path.join(folder_abs, filename)
            file_paths.append(file_abs)

    if not file_paths:
        print(f"提示：文件夾 {folder_abs} 里沒有.{filetype}文件！")
        return None
    return file_paths

# ===================== 独立函数：資料夾檢查 =====================
def check_folders(folder_abs):
    """
    筛选文件夹下的非隐藏子文件夹
    :param folder_abs: 文件夹绝对路径
    :return: 子文件夹绝对路径列表
    """
    subfolder_paths = []
    for foldername in os.listdir(folder_abs):
        folder_item = os.path.join(folder_abs, foldername)
        if os.path.isdir(folder_item) and not foldername.startswith("."):
            subfolder_paths.append(folder_item)
    return subfolder_paths

# ===================== 独立函数：分类文件 =====================
def classify_files(files, prefix, filetype, pattern=r"\d+"):
    """
    分類文件：保留「前綴+_+數字.文件類型」的文件，其餘為待重命名文件
    :param files: 所有目标类型文件列表
    :param prefix: 新文件名前綴（如Document）
    :param filetype: 文件类型（如txt）
    :param pattern: 匹配數字的正則表達式
    :return: (reserved_files, to_rename_files) 保留文件列表、待重命名文件列表
    """
    reserved_files = []
    to_rename_files = []
    # 转义前缀中的特殊正则字符（如.、*等）
    escaped_prefix = re.escape(prefix)
    # 构建正则表达式
    regex_pattern = rf"{escaped_prefix}_({pattern})\.{filetype}$"

    for file in files:
        # 匹配文件basename（避免路径中的字符干扰）
        file_basename = os.path.basename(file)
        if re.match(regex_pattern, file_basename):
            reserved_files.append(file)
        else:
            to_rename_files.append(file)
    return reserved_files, to_rename_files

    '''    
    保留文件列表 = []
    待重命名列表 = []
    匹配規則 = "前綴_數字.文件類型"  # 比如 "Document_0.txt"

    對每一個文件做檢查：
        如果文件名符合「匹配規則」→ 放進保留列表；
        否則 → 放進待重命名列表；

    返回 保留列表, 待重命名列表
    '''
# ===================== 独立函数：收集已用序号 =====================
def collect_used_numbers(reserved_files, prefix, filetype, pattern=r"\d+"):
    """
    收集保留文件中已使用的數字序號
    :param reserved_files: 保留文件列表
    :param prefix: 文件名前綴
    :param filetype: 文件类型（如txt）
    :param pattern: 匹配數字的正則表達式
    :return: 已使用的序號集合（如{0,1}）
    """
    used_nums = set()
    escaped_prefix = re.escape(prefix)
    regex_pattern = rf"{escaped_prefix}_({pattern})\.{filetype}$"

    for res_file in reserved_files:
        file_basename = os.path.basename(res_file)
        match = re.match(regex_pattern, file_basename)
        if match:
            num = int(match.group(1))
            used_nums.add(num)
    return used_nums

    '''
    已用編號小本本 = 空本子
    匹配規則 = "前綴_數字.文件類型"

    對每一個保留文件：
        從文件名里扒出數字（比如從Document_1.txt里扒出1）；
        把數字寫進小本本；

    返回 已用編號小本本
    '''

# ===================== 独立函数：生成重命名映射 =====================
def generate_rename_mapping(to_rename_files, prefix, used_nums, filetype):
    """
    生成「舊路徑→新路徑」的映射表，分配不重複的序號
    :param to_rename_files: 待重命名文件列表
    :param prefix: 新文件名前綴
    :param used_nums: 已使用的序號集合
    :param filetype: 文件类型（如txt）
    :return: 重命名映射字典
    """
    rename_mapping = {}
    current_num = 0

    for old_path in to_rename_files:
        # 找到最小的未使用序号
        while current_num in used_nums:
            current_num += 1
        # 生成新文件名
        new_name = f"{prefix}_{current_num}.{filetype}"
        new_path = os.path.join(os.path.dirname(old_path), new_name)
        rename_mapping[old_path] = new_path
        used_nums.add(current_num)
        current_num += 1
    return rename_mapping

    '''
    改名名單 = 空名單
    當前編號 = 0

    對每一個待重命名文件：
        重複檢查：如果當前編號在小本本里 → 編號+1（比如0被用了→1，1被用了→2）；
        新文件名 = 前綴 + "_" + 當前編號 + "." + 文件類型；
        新路徑 = 原文件所在文件夾 + 新文件名；
        把「舊路徑→新路徑」寫進改名名單；
        把當前編號記進小本本；
        當前編號+1；

    返回 改名名單
    '''

# ===================== 独立函数：执行重命名 =====================
def execute_rename(rename_mapping):
    """
    執行重命名操作，返回成功/失敗數量
    :param rename_mapping: 重命名映射字典 {old_path: new_path}
    :return: (success, fail) 成功數量、失敗數量
    """
    success = 0
    fail = 0
    for old_path, new_path in rename_mapping.items():
        old_file = os.path.basename(old_path)
        new_file = os.path.basename(new_path)
        try:
            os.rename(old_path, new_path)
            print(f"成功：{old_file} → {new_file}")
            success += 1
        except Exception as e:
            print(f"失敗：{old_file} → {new_file} 錯誤：{e}")
            fail += 1
    return success, fail

    '''
    成功數 = 0
    失敗數 = 0

    對名單里的每一條記錄：
        嘗試把「舊文件名」改成「新文件名」；
        如果改成功 → 成功數+1，打印「改好了」；
        如果改失敗 → 失敗數+1，打印「改壞了，原因是XXX」；

    返回 成功數, 失敗數
    '''

# ===================== 独立函数：鑑別特定檔案 =====================
def filter_files_by_keyword(files, keyword):

    """
    根據關鍵字篩選文件
    :param files: 文件列表
    :param keyword: 關鍵字
    :return: 包含關鍵字的文件列表
    """
    filtered_files = [p for p in files if keyword in os.path.basename(p)]
    return filtered_files

# ===================== 处理单个文件夹的重命名逻辑 =====================
def process_single_folder(folder_abs, prefix, filetype):
    """
    处理单个文件夹的重命名逻辑
    :param folder_abs: 文件夹绝对路径
    :param prefix: 文件名前缀
    :param filetype: 文件类型
    :return: (reserved_count, to_rename_count, success, fail) 统计数据
    """
    # 1. 获取当前文件夹下的目标文件
    files = check_files(folder_abs, filetype)
    if not files:
        return 0, 0, 0, 0

    # 2. 分类文件
    reserved_files, to_rename_files = classify_files(files, prefix, filetype)
    reserved_count = len(reserved_files)
    to_rename_count = len(to_rename_files)

    # 无待重命名文件则直接返回
    if to_rename_count == 0:
        print(f"\n文件夾 {folder_abs} 無需重命名的文件：{[os.path.basename(f) for f in reserved_files]}")
        return reserved_count, 0, 0, 0

    # 3. 确认是否继续
    print(f"\n文件夾 {folder_abs} 檢測到：")
    print(f"- 無需重命名的文件：{[os.path.basename(f) for f in reserved_files]}")
    print(f"- 待重命名的文件：{[os.path.basename(f) for f in to_rename_files]}")
    print(f"\n即將重命名 {to_rename_count} 個文件，是否繼續？(y/n)")
    confirm = input().strip().lower()
    if confirm != "y":
        print(f"文件夾 {folder_abs} 操作取消！")
        return reserved_count, to_rename_count, 0, 0

    # 4. 收集已用序号
    used_nums = collect_used_numbers(reserved_files, prefix, filetype)

    # 5. 生成重命名映射
    rename_mapping = generate_rename_mapping(to_rename_files, prefix, used_nums, filetype)

    # 6. 执行重命名
    success, fail = execute_rename(rename_mapping)
    return reserved_count, to_rename_count, success, fail

# ===================== 主逻辑 =====================
def batch_rename(root_folder, prefix="file"):
    """
    批量重命名主函數（支持递归处理子文件夹）
    :param root_folder: 根文件夹路径
    :param prefix: 新文件名前綴
    """
    # 0. 获取文件类型
    filetype = what_is_the_filetype()

    # 1. 校验根文件夹
    root_folder_abs = validate_folder_and_files(root_folder, filetype)
    if not root_folder_abs:
        return

    # 初始化全局统计
    total_reserved = 0
    total_to_rename = 0
    total_success = 0
    total_fail = 0

    # 2. 处理根文件夹
    print(f"\n===== 處理根文件夾：{root_folder_abs} =====")
    reserved, to_rename, success, fail = process_single_folder(root_folder_abs, prefix, filetype)
    total_reserved += reserved
    total_to_rename += to_rename
    total_success += success
    total_fail += fail

    # 3. 处理子文件夹
    subfolders = check_folders(root_folder_abs)
    if subfolders:
        for subfolder in subfolders:
            print(f"\n===== 處理子文件夾：{subfolder} =====")
            reserved, to_rename, success, fail = process_single_folder(subfolder, prefix, filetype)
            total_reserved += reserved
            total_to_rename += to_rename
            total_success += success
            total_fail += fail

    # 4. 打印全局统计结果
    print("\n=== 全局重命名結果 ===")
    print(f"總保留文件數：{total_reserved}")
    print(f"總待重命名文件數：{total_to_rename}")
    print(f"總重命名成功：{total_success} 個")
    print(f"總重命名失敗：{total_fail} 個")

# ===================== 命令行入口 =====================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="批量重命名工具（支持递归处理子文件夹）")
    parser.add_argument("--folder", required=True, help="根文件夾路徑")
    parser.add_argument("--prefix", default="file", help="新文件名前綴")
    args = parser.parse_args()
    batch_rename(args.folder, args.prefix)
