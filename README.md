局域网分组投票系统 - 部署与使用指南
本系统专为无外网环境（如学校机房、教室局域网）设计，无需互联网，无需安装数据库，仅需一台老师电脑即可运行。

📁 1. 文件准备
请在桌面上新建一个文件夹（例如命名为 vote），确保文件夹内包含以下 3 个文件：
1. main.py (后端核心)
  - 负责处理投票逻辑、WebSocket 通信和网页托管。
  - 确保代码中包含了 /screen 的路由配置。
2. index.html (学生端/控制端)
  - 学生用于投票。
  - 老师用于“新建投票”（点击时需输入密码）。
3. screen.html (大屏展示端)
  - 纯净的显示界面，只展示实时结果。
  - 包含“结束投票”按钮（需要密码）。
🛠️ 2. 环境安装 (仅首次需要)
在老师的电脑上安装 Python (建议 3.8 或以上版本)。 打开命令行工具 (Win+R 输入 cmd)，运行以下命令安装依赖库：
pip install fastapi uvicorn websockets
🚀 3. 启动系统 (每次上课前)
1. 进入存放文件的文件夹 (vote)。
2. 在文件夹空白处按住 Shift + 右键，选择 “在此处打开 Powershell 窗口” (或命令行)。
3. 输入启动命令并回车：
uvicorn main:app --host 0.0.0.0 --port 8000
看到 Application startup complete 字样即表示启动成功。请勿关闭此黑色窗口。
🏫 4. 上课使用流程 (角色分配)
第一步：获取老师 IP 地址
- 打开新的命令行窗口，输入 ipconfig (Windows) 或 ifconfig (Mac)。
- 记录下 IPv4 地址 (例如: 192.168.1.5)。
第二步：老师发布投票 (控制端)
1. 老师在自己电脑浏览器打开：http://localhost:8000
2. 点击右上角的 “老师新建” 按钮。
3. 立刻输入管理员密码 (默认: 8888)，密码验证通过后才会显示创建表单。
4. 填写问题和选项，点击 “发布” 按钮（此时将自动发布，无需再次输入密码）。
 <img width="2382" height="539" alt="屏幕截图 2025-12-15 235901" src="https://github.com/user-attachments/assets/e3e2f9ea-8d97-4e27-a416-93141be56d8a" />
<img width="1669" height="431" alt="屏幕截图 2025-12-15 235931" src="https://github.com/user-attachments/assets/d0d35477-fa79-4464-b1f4-8f7a3f1cac76" />
<img width="2682" height="1057" alt="屏幕截图 2025-12-15 234828" src="https://github.com/user-attachments/assets/49d852be-c0b8-4753-8973-61e0b91e3178" />

  

 
第三步：开启大屏展示 (大屏端)
1. 将连接投影仪/大屏幕的显示器设置为扩展或复制模式。
2. 在大屏浏览器访问：http://localhost:8000/screen
  - 或者使用 IP 访问：http://192.168.1.5:8000/screen
3. 按 F11 全屏显示。此时屏幕上会显示刚才创建的投票结果（初始为0）。
<img width="2063" height="975" alt="屏幕截图 2025-12-16 000058" src="https://github.com/user-attachments/assets/0f5726c7-28b4-4e7e-9dd7-fe04de2dee8b" />

第四步：学生投票 (学生端)
1. 学生手机/电脑连接与老师相同的 Wi-Fi。
2. 学生在浏览器输入老师的 IP 地址：http://192.168.1.5:8000
  - 注意：学生不需要输入 /screen，直接访问根路径即可。
3. 学生选择组别 -> 选择选项 -> 提交。
4. 大屏幕实时滚动更新数据。
<img width="1632" height="1443" alt="屏幕截图 2025-12-16 000122" src="https://github.com/user-attachments/assets/3da66e2f-7f55-4bec-a409-df632b52947d" />

⚠️ 5. 结束投票
当投票结束，需要开启下一轮时：
1. 老师可以在 大屏端页面 (/screen) 右下角点击 “结束投票”。
2. 或者在 控制端页面 (/) 点击结束。
3. 输入管理员密码 (默认: 8888)。
4. 数据清空，系统回到等待状态，可以重新创建新投票。
 <img width="1626" height="1475" alt="屏幕截图 2025-12-16 000140" src="https://github.com/user-attachments/assets/9b64c512-f780-4cc9-8c6e-1daffc9e4ff8" />

❓ 常见问题
Q: 学生打不开网页？ A:
1. 检查学生是否连接了和老师同一个 Wi-Fi。
2. 检查老师电脑的防火墙是否拦截了 8000 端口（尝试暂时关闭防火墙）。
3. 确认 IP 地址是否输入正确。
Q: 怎么修改密码？ A: 用记事本打开 main.py，找到 ADMIN_PASSWORD = "8888"，修改引号里的数字并保存，重启服务器即可。
Q: 点击“老师新建”没有反应？ A: 请检查浏览器是否拦截了弹窗。通常点击按钮触发的弹窗不会被拦截，如果没反应，请尝试刷新页面。
