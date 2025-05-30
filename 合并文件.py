import os, glob

# 目标目录（可修改为相对路径或绝对路径）
dir_path = "./不死仙帝"

# 获取目标目录的绝对路径
abs_path = os.path.abspath(dir_path)

# 获取父目录路径和目标目录名称
parent_dir = os.path.dirname(abs_path)
dir_name = os.path.basename(abs_path)

# 创建输出文件路径（保存在父目录）
out_file = os.path.join(parent_dir, f"{dir_name}.txt")

# 获取并排序txt文件
os.chdir(dir_path)
# files = sorted(glob.glob("*.txt"), key=os.path.getmtime) # 时间排序，启用请注释掉下一行代码
files = sorted(glob.glob("*.txt"), key=lambda f: int(f.split('.')[0])) # 前缀排序

# 合并文件
with open(out_file, "w") as f_out:
    for file in files:
        with open(file) as f_in:
            # 修改点：使用文件名作为分隔符
            f_out.write(f"\n\n===== {file.removesuffix(".txt")[2:]} =====\n\n") # 删除前两个字符（前缀）
            # f_out.write(f"\n\n===== {file.removesuffix(".txt")} =====\n\n")
            f_out.write(f_in.read())

print(f"合并完成: 共合并 {len(files)} 个文件")
print(f"保存位置: {out_file}")
