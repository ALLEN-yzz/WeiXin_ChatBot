# 部署流程文档

本文档详细介绍了微信采样点查询机器人的部署步骤和注意事项。

## 系统要求

- **操作系统**：Windows 7/8/10/11
- **Python版本**：Python 3.7 或更高版本
- **微信客户端**：最新版本的微信Windows客户端
- **硬件要求**：至少4GB内存，足够的存储空间

## 安装步骤

### 1. 安装Python

如果您的系统尚未安装Python，请按照以下步骤安装：

1. 访问 [Python官方网站](https://www.python.org/downloads/)
2. 下载最新的Python 3.x版本
3. 运行安装程序，确保勾选 "Add Python to PATH"
4. 完成安装后，打开命令提示符验证安装：
   ```bash
   python --version
   ```
   您应该看到类似 `Python 3.10.x` 的输出。

### 2. 下载项目代码

#### 方法A：使用Git克隆（推荐）

```bash
# 克隆仓库
git clone <your-github-repo-url>

# 进入项目目录
cd <project-directory>
```

#### 方法B：下载ZIP文件

1. 在GitHub仓库页面点击 "Code" 按钮
2. 选择 "Download ZIP"
3. 解压下载的ZIP文件到您选择的目录

### 3. 安装项目依赖

打开命令提示符，导航到项目目录，然后运行：

```bash
# 创建虚拟环境（可选但推荐）
python -m venv venv

# 激活虚拟环境
# Windows命令提示符
env\Scripts\activate
# 或 Windows PowerShell
./venv/Scripts/Activate.ps1

# 安装依赖
pip install -r requirements.txt
```

### 4. 准备知识库

项目包含`sampling_knowledge_base_example.json`作为示例知识库，您需要创建自己的知识库：

1. **复制示例文件**：
   - 将`sampling_knowledge_base_example.json`复制并重命名为`sampling_knowledge_base.json`
   - 或者创建一个新的JSON文件，文件名设为`sampling_knowledge_base.json`

2. **编辑知识库内容**：
   - 打开您的知识库文件
   - 按照示例格式添加您自己的问答对
   - 确保JSON格式正确，特别是换行符使用`\n`转义

3. **更新代码配置**（如需要）：
   - 在`WeChatBot copy.py`中确认`KNOWLEDGE_BASE_FILE`变量指向正确的知识库文件名

### 5. 准备微信客户端

1. 确保您已在Windows上安装微信客户端
2. 登录您的微信账号
3. 保持微信窗口在桌面可见状态

## 运行程序

### 方法A：命令行运行

```bash
python "WeChatBot copy.py"
```

### 方法B：双击运行

在文件资源管理器中找到`WeChatBot copy.py`文件，直接双击运行。

## 故障排除

### 常见问题及解决方案

1. **"无效的窗口句柄"错误**
   - 确保微信客户端已登录并在桌面上可见
   - 尝试重启微信客户端和程序
   - 检查微信是否为最新版本

2. **JSON解析错误**
   - 检查`sampling_knowledge_base.json`文件格式是否正确
   - 确保所有字符串都使用双引号
   - 确保换行符使用`\n`而不是实际换行
   - 可以使用在线JSON验证工具检查文件格式

3. **依赖安装失败**
   - 确保pip已更新：`pip install --upgrade pip`
   - 尝试使用管理员权限运行命令提示符
   - 检查网络连接是否正常

4. **找不到知识库文件**
   - 确保已创建`sampling_knowledge_base.json`文件
   - 检查文件名拼写是否正确
   - 确认知识库文件与程序位于同一目录

## 部署到生产环境（可选）

### 创建快捷方式

1. 右键点击`WeChatBot copy.py`文件
2. 选择"发送到" > "桌面快捷方式"
3. 右键点击桌面上的快捷方式，选择"属性"
4. 在"目标"字段后添加适当的工作目录参数

### 配置自动启动

#### 方法A：任务计划程序

1. 打开"任务计划程序"
2. 点击"创建基本任务"
3. 按照向导设置触发器（如登录时）和操作（启动Python脚本）
4. 在"操作"中，程序/脚本设置为`python.exe`的完整路径，添加参数为脚本的完整路径

#### 方法B：启动文件夹

1. 按`Win + R`打开运行对话框
2. 输入`shell:startup`并按回车
3. 将程序的快捷方式复制到打开的文件夹中

## 更新项目

如果您使用Git克隆了项目，可以通过以下命令更新：

```bash
git pull origin main
pip install -r requirements.txt  # 安装可能的新依赖
```

## 安全注意事项

- 请勿在公共场所的计算机上登录您的微信账号运行此程序
- 定期更新微信客户端和项目依赖
- 保护好您的知识库文件，不要在其中存储敏感或机密信息
- 示例知识库仅供演示使用，生产环境请使用您自己的安全数据
- 不要将包含敏感信息的知识库文件提交到版本控制系统中

---

如果您在部署过程中遇到任何问题，请参考[GitHub Issues页面](https://github.com/your-username/your-repo-name/issues)或创建一个新的Issue。