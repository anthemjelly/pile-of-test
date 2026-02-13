import argparse

import rename


def test_validate_folder_and_files(folder, prefix, filetype="txt"):
    result = rename.validate_folder_and_files(folder, filetype)
    return result


if __name__ == "__main__":
    # 🚨 命令行參數解析（可單獨复用於其他命令行工具）
    parser = argparse.ArgumentParser(description="批量重命名工具（獨立函數版）")
    parser.add_argument("--folder", required=True, help="文件夾路徑")
    parser.add_argument("--prefix", default="file", help="新文件名前綴")
    args = parser.parse_args()
    # 調用主函數
    result = test_validate_folder_and_files(args.folder, args.prefix)
    print("測試結果：", result)
