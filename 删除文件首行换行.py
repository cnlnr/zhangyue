import os

def process_txt_files(folder_path):
    """
    遍历文件夹中的.txt文件，删除第一行的换行符（如果只有换行符）
    否则打印警告信息
    """
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                try:
                    # 读取文件内容
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    
                    # 检查文件是否为空
                    if not lines:
                        print(f"文件为空: {file_path}")
                        continue
                    
                    # 处理第一行
                    if lines[0] == '\n':  # 第一行只有换行符
                        # 删除第一行并重写文件
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.writelines(lines[1:])
                    else:
                        # 打印警告
                        print(f"警告: {file_path} 首行不是空行")
                except Exception as e:
                    print(f"处理文件 {file_path} 出错: {str(e)}")

if __name__ == "__main__":
    target_folder = "不死仙帝"
    
    if os.path.isdir(target_folder):
        process_txt_files(target_folder)
        print("\n处理完成!")
    else:
        print("错误: 路径不是有效的文件夹")
